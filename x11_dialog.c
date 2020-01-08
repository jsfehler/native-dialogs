#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <X11/X.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

Display* safe_open_display(const char* screen);

/* Try to open a display. Exit if it fails. */
Display* safe_open_display(const char* screen) {
    Display* display;
    
    display = XOpenDisplay(screen);
    if (display == NULL) {
        fprintf(stderr, "Cannot connect to X server: %s \n", screen);
        exit(-1);
    }
    
    return(display);
}


/* Button handler */
typedef struct {
    Display *display;
    Window window;
    GC gc;
    char *text;
    XFontStruct *font_info;
    int mouseover;
    int clicked;
    int x, y;
    unsigned int width, height;
    int text_x, text_y;
    
} X11Button;


static int is_point_inside(X11Button* btn, int px, int py) {
    return px>=btn->x && px<=(btn->x + (int)btn->width-1) &&
           py>=btn->y && py<=(btn->y + (int)btn->height-1);
}


/* Set button size and location. */ 
void button_set_area(X11Button *btn, XWindowAttributes window_attributes, int x, int y) {   
    int direction;
    int ascent;
    int descent;
    XCharStruct text_structure;

    XTextExtents(
        btn->font_info,
        btn->text,
        strlen(btn->text),
        &direction,
        &ascent,
        &descent,
        &text_structure
    );

    btn->width = text_structure.width + 30;
    btn->height = ascent + descent + 5;
    btn->x = x - (btn->width / 2);
    btn->y = y;
    btn->text_x = btn->x + 15;
    btn->text_y = btn->y + btn->height - 3;

    XFreeFontInfo(NULL, btn->font_info, 1);
}


static void button_draw(
    X11Button *btn,
    int foreground,
    int background) {

    if (btn->mouseover) {
        XFillRectangle(
            btn->display,
            btn->window,
            btn->gc,
            btn->clicked + btn->x,
            btn->clicked + btn->y,
            btn->width,
            btn->height
        );
        /*XSetForeground(display, gc, background);
        XSetBackground(display, gc, foreground);*/

    } else {
        /*XSetForeground(display, gc, foreground);
        XSetBackground(display, gc, background);*/
        XDrawRectangle(
            btn->display,
            btn->window,
            btn->gc,
            btn->x,
            btn->y,
            btn->width,
            btn->height
        );
    }

    XDrawString(
        btn->display,
        btn->window,
        btn->gc,
        btn->clicked + btn->text_x,
        btn->clicked + btn->text_y,
        btn->text,
        strlen(btn->text)
    );
    
    /*XSetForeground(display, gc, foreground);
    XSetBackground(display, gc, background);*/
}


bool button_event_buttonrelease(X11Button *btn, XEvent ev) {
    /* Ignore everything but the left mouse button. */
    if (ev.xbutton.button != Button1){
        return(false);
    }
    
    if(btn->mouseover) {
        btn->clicked = ev.type == ButtonPress ? 1 : 0;

        if (!btn->clicked) {
            XFreeGC(btn->display, btn->gc);
            XDestroyWindow(btn->display, btn->window);
            XCloseDisplay(btn->display);
            return(true);
        }
    }
    else {
        btn->clicked = 0;
    }
    
    return(false);
}


/* Create a small, non-resizeable box to display messages. */
int MessageBox(const char* text, const char* title) {
    Display* display;
    int black_pixel;
    int white_pixel;
    GC gc;
    Window window;
    XEvent event;
    XFontStruct *font_info;
    XGCValues gc_values;
    XSizeHints hints;
    Atom wmDelete;
    char *atom;

    const char *end, *temp;
    size_t i, lines = 0;

    display = safe_open_display(0);

    black_pixel = BlackPixel(display, DefaultScreen(display));
    white_pixel = WhitePixel(display, DefaultScreen(display));

    window = XCreateSimpleWindow(
        display,
        RootWindow(display, 0),
        0, 0, 10, 10,
        0,
        black_pixel,
        white_pixel
    );
    
    /* Listen for input */
    XSelectInput(
        display,
        window,
        ExposureMask | StructureNotifyMask | KeyReleaseMask | PointerMotionMask |
        ButtonPressMask | ButtonReleaseMask
    );

    XMapWindow(display, window);
    
    /* Set the title for the box. */
    XStoreName(display, window, title);
    
    /* Allow window to be closed by pressing the cross button. */
    wmDelete = XInternAtom(display, "WM_DELETE_WINDOW", true);
    XSetWMProtocols(display, window, &wmDelete, 1);
    
    /* Try to get a font. */
    font_info = XLoadQueryFont(display, "6x13");
    if (!font_info) {
        fprintf(stderr, "Failed loading font \n");
        exit(-1);
    }

    gc_values.font = font_info->fid;
    gc_values.foreground = black_pixel;
    
    /* Create graphical context */
    gc = XCreateGC(
        display,
        window,
        GCFont + GCForeground,
        &gc_values
    );

    /* Calculate the window size based on the text width and height. */
    XWindowAttributes window_attributes;

    int window_w = 0, window_h = 0;
    int window_x, window_y;
    int height = 0;

    int direction;
    int ascent;
    int descent;
    XCharStruct overall;
    
    for(temp = text; temp; temp = end ? (end+1) : NULL, ++lines ) {
        end = strchr(temp, '\n');
        
        XTextExtents(
            font_info,
            temp,
            end ? (unsigned int)(end-temp):strlen(temp),
            &direction,
            &ascent,
            &descent,
            &overall
        );

        window_w = overall.width>window_w ? overall.width : window_w;
        height = (ascent + descent)>height ? (ascent + descent) : height;
    }
    
    window_w += 10;
    window_h = lines * height + height + 40;

    /* Place the window in the center of the screen. */
    window_x = DisplayWidth(display, DefaultScreen(display) ) / 2 - (window_w / 2);
    window_y = DisplayHeight(display, DefaultScreen(display) ) / 2 - (window_h / 2);
    
    XMoveResizeWindow(display, window, window_x, window_y, window_w, window_h);    
    
    XGetWindowAttributes(display, window, &window_attributes);  
    
    /* XSetFont(display, gc, font_info->fid ) */
    
    /* TODO: Create as many buttons as desired. Customize label.*/
    X11Button x11_button;
    x11_button.display = display;
    x11_button.window = window;
    x11_button.gc = gc;
    x11_button.text = "OK";
    x11_button.font_info = font_info;
    x11_button.mouseover = 0;

    button_set_area(&x11_button, window_attributes, window_w / 2, window_h - height - 15);

    /* Make the window non resizeable */
    XUnmapWindow(display, window);

    hints.flags = PSize | PMinSize | PMaxSize;
    hints.min_width = hints.max_width = hints.base_width  = window_w;
    hints.min_height = hints.max_height = hints.base_height = window_h;

    XSetWMNormalHints(display, window, &hints);
    XMapRaised(display, window);

    XFlush(display);

    bool quit = false;

    while (!quit) {
        XNextEvent(display, &event);
        
        x11_button.clicked = 0;

        if(event.type == MotionNotify) {
            if(is_point_inside(&x11_button, event.xmotion.x, event.xmotion.y)) {
                if(!x11_button.mouseover) {
                    event.type = Expose;
                }
                x11_button.mouseover = 1;
            } else {
                if(x11_button.mouseover) {
                    event.type = Expose;
                }

                x11_button.mouseover = 0;
                x11_button.clicked = 0;
            }
        }

        switch (event.type) {
            case ButtonPress:
            case ButtonRelease:
                if (button_event_buttonrelease(&x11_button, event)) {
                    quit = true;
                    break;
                }
                
            case Expose:
            case MapNotify:
                XClearWindow(display, window);

                for(i=0, temp=text; temp; temp=end ? (end+1) : NULL, i+=height ) {
                    end = strchr(temp, '\n');
                    XDrawString(
                        display,
                        window,
                        gc,
                        10,
                        10+height+i,
                        temp,
                        end ? (unsigned int)(end-temp) : strlen(temp)
                    );
                }

                button_draw(
                    &x11_button,
                    white_pixel,
                    black_pixel
                );

                XFlush(display);

                break;
    
            /* Closing MessageBox from the window's cross button */
            case ClientMessage:
                atom = XGetAtomName(display, event.xclient.message_type);
                if (*atom == *"WM_DELETE_WINDOW") {
                    XFreeGC(display, gc);
                    XDestroyWindow(display, window);
                    XCloseDisplay(display);
                    quit = true;
                }

                XFree(atom);
                break;
        }
    }
    
    return(0);
}
