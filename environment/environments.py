#!/usr/bin/python

from lxml import etree
import sys

import pygtk
pygtk.require('2.0')
import gtk

class ApplicationVersion:

    def __init__(self, version_node):
        self.title = version_node.get("title")
        self.default = version_node.get("default") == "true"

    def __str__(self):
        return self.title

class Application:

    def __init__(self, application_node):
        self.title = application_node.get("title")
        self.versions = []
        self.selected_version = None

        for version_node in application_node.xpath("./version"):
            application_version = ApplicationVersion(version_node)
            self.versions.append(  application_version )
            if application_version.default:
                self.selected_version = application_version

    def do_version_selected(self, button, version):
        print "Version Selected", version
        self.selected_version = version

class Environment:

    def __init__(self, environment_node):
        self.id = environment_node.get("id")
        self.name = environment_node.get("name")
        self.applications = []

        for application_node in environment_node.xpath("./application"):
            self.applications.append(  Application(application_node) )

class Environments:

    def __init__(self, environments_filename):
        self.environments = []
        self.selected_environment = None

        tree = etree.parse(environments_filename)
        for environment_node in tree.xpath("/environments/environment"):
            environment = Environment(environment_node)
            self.environments.append(environment)
            if self.selected_environment == None:
                self.selected_environment = environment

    def do_environment_select(self, notebook, page, page_num):
        print "Page_num", page_num
        self.selected_environment = self.environments[page_num]

class EnvironmentSelector:

    def callback(self, widget, data=None):
        print "Hello again - %s was pressed" % data

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):

        self.environments = Environments(sys.argv[1])

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Hello Buttons!")
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(10)

        self.notebook = gtk.Notebook()
        self.window.add(self.notebook)

        for environment in self.environments.environments:
            tab_label = gtk.Label(environment.name)
            tab_pane_box = gtk.VBox(False, 0)
            
            for application in environment.applications:
                application_label = gtk.Label(application.title)
                application_label.show()
                application_alignment = gtk.Alignment(xalign=0, xscale=0)
                application_alignment.add(application_label)
                application_alignment.show()
                tab_pane_box.pack_start(application_alignment, expand=False, padding=5)

                application_hbox = gtk.HBox(False, 0)
                application_hbox.show()
                tab_pane_box.pack_start(application_hbox, expand=False, padding=0)
                
                radio_button_group = gtk.RadioButton(None, "None")
                radio_button_group.show();
                radio_button_group.connect_object("toggled", application.do_version_selected, radio_button_group, None)
                application_hbox.pack_start(radio_button_group, expand=False, padding=5)

                for version in application.versions:
                    version_radiobutton = gtk.RadioButton(radio_button_group, version.title)
                    version_radiobutton.show()
                    version_radiobutton.connect_object("toggled", application.do_version_selected, version_radiobutton, version)
                    application_hbox.pack_start(version_radiobutton, expand=False, padding=5)
                    if version.default:
                        version_radiobutton.set_active(True)
                
            self.notebook.append_page( tab_pane_box, tab_label=tab_label)
            
            tab_label.show()
            tab_pane_box.show()

        self.notebook.connect_object("switch-page", self.environments.do_environment_select, None)
        self.notebook.show()
        self.window.show()

    def main(self):
        gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    selector = EnvironmentSelector()
    selector.main()
