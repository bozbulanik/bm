"""
cli tool to add bookmarks to db individually or as a batch from bookmark files extracted from browsers

todo:
see bookmarks in a folder like structure
ability to move bookmarks between folders
search bookmarks

"""
import urwid as u
import json
import webbrowser

class ListItem(u.WidgetWrap):
    def __init__ (self, bookmark, actions=None):
        self.content = bookmark
        self.actions = actions or []
        self.update_display()

    def update_display(self):
        """Update the display to show * if there are actions."""
        name = self.content["title"]
        if self.actions:
            if("delete" in self.actions):
                name = "Will be deleted: " + name  # Add * to indicate pending actions
            else:
                name = "* " + name  # Add * to indicate pending actions
            t = u.AttrWrap(u.Text(name, wrap="clip"), "item_action", "item_selected_action")
        else:
            t = u.AttrWrap(u.Text(name, wrap="clip"), "item", "item_selected")

        self._w = t  # Update the widget
        
    def selectable (self):
        return True
    
    def keypress(self, size, key):
        if key == 'd':  # Add action 'delete'
            self.actions.append('delete')
            self.update_display()  # Update display with *
            return 'action_added'
        elif key == 'z':  # Remove the most recent action
            if self.actions:
                self.actions.pop()
            self.update_display()
            return 'action_removed'
        elif key == 'o':  # Confirm actions
            return 'confirm'
        elif key == 'enter':
            url = self.content.get('url')
            if url:
                webbrowser.open(url)  # Open the bookmark URL in the browser
            return 'open_browser'
        return key

class ListView(u.WidgetWrap):
    def __init__(self):
        u.register_signal(self.__class__, ['show_details', 'item_action', 'confirm_actions'])
        self.walker = u.SimpleFocusListWalker([])
        lb = u.ListBox(self.walker)
        u.WidgetWrap.__init__(self, lb)

    def keypress(self, size, key):
        focus_w, focus_pos = self.walker.get_focus()
        if focus_w:
            action = focus_w.keypress(size, key)
            if action == 'action_added' or action == 'action_removed':
                next_pos = (focus_pos + 1) % len(self.walker)  # Get the next position, wrap around if at the end
                self.walker.set_focus(next_pos)  # Move focus to the next item
                u.emit_signal(self, 'item_action', action)
            elif action == 'confirm':
                u.emit_signal(self, 'confirm_actions')
            else:
                return super().keypress(size, key)
                
    def modified(self):
        focus_w, _ = self.walker.get_focus()
        u.emit_signal(self, 'show_details', focus_w.content)

    def set_data(self, bookmarks):
        bookmarks_widgets = [ListItem(b) for b in bookmarks]
        u.disconnect_signal(self.walker, 'modified', self.modified)
        
        while len(self.walker) > 0:
            self.walker.pop()
        
        self.walker.extend(bookmarks_widgets)
        u.connect_signal(self.walker, "modified", self.modified)
        self.walker.set_focus(0)

class DetailView(u.WidgetWrap):
    def __init__ (self):
        t = u.Text("")
        u.WidgetWrap.__init__(self, t)
        
    def set_bookmark(self, c):
        s = f'{c["title"]}\n\n{c["url"]}\n\n{c["added_on"]}'
        self._w.set_text(s)

class App(object):
    def unhandled_input(self, key):
        if key in ('q','Q'):
            raise u.ExitMainLoop()

    def show_details(self, bookmark):
        self.detail_view.set_bookmark(bookmark)

    def handle_keypress(self, action):
        focus_w, _ = self.list_view.walker.get_focus()
        if not focus_w:
            return
        bookmark = focus_w.content
        url = bookmark["url"]

        if action == 'action_added':
            if url not in self.actions_dict:
                self.actions_dict[url] = []
            focus_w.actions = self.actions_dict[url]  # Sync the actions
        elif action == 'action_removed':
            if url in self.actions_dict and not focus_w.actions:
                del self.actions_dict[url]
    
    def confirm_actions(self):
        """Process and apply all the actions."""
        for url, actions in self.actions_dict.items():
            for action in actions:
                if action == 'delete':
                    print(f"Deleting bookmark: {url}")
                    # Implement the delete logic here

        # After confirming, clear the actions
        self.actions_dict.clear()
        self.update_data()
            
    def __init__(self):
        self.palette = {
            ("bg",                      "light gray",       "black"),
            ("item",                    "light gray",       "black"),
            ("item_action",             "light gray",       "light blue"),
            ("item_selected",           "light gray",       "dark red"),
            ("item_selected_action",    "black",       "yellow"),
            ("footer",                  "black",            "light gray")
        }
        self.actions_dict = {}
        self.list_view = ListView()
        self.detail_view = DetailView()

        u.connect_signal(self.list_view, 'show_details', self.show_details)
        u.connect_signal(self.list_view, 'item_action', self.handle_keypress)
        u.connect_signal(self.list_view, 'confirm_actions', self.confirm_actions)
        
        footer = u.AttrWrap(u.Text(" q to exit | d: delete | o: open"), "footer") 
        
        col_rows = u.raw_display.Screen().get_cols_rows()
        h = col_rows[0] - 2
                
        f1 = u.Filler(self.list_view, valign='top', height=h)
        f2 = u.Filler(self.detail_view, valign='top')

        c_list = u.LineBox(f1, title="Bookmarks")
        c_details = u.LineBox(f2, title="Details")
        
        columns = u.Columns([('weight', 70, c_list), ('weight', 30, c_details)])            

        frame = u.AttrMap(u.Frame(body=columns, footer=footer), 'bg')
        
        self.loop = u.MainLoop(frame, self.palette, unhandled_input=self.unhandled_input)

    def update_data(self):
        l = []
        with open('UNIQUE_BOOKMARKS.json', 'r') as file:
            l = json.load(file)
            
        
        
        
        self.list_view.set_data(l)

    def start(self):

        self.update_data()
        self.loop.run()

if __name__ == '__main__':

    app = App()
    app.start()
