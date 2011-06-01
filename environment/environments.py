#!/usr/bin/python

from lxml import etree
import sys

import pygtk
pygtk.require('2.0')
import gtk

class SetVariable:

    def __init__(self, command_node):
        self.variable_name = command_node.get("name")
        self.variable_value = command_node.text

    def __str__(self):
        return self.variable_name + "=" + self.variable_value

    def execute(self):
        public_variables[self.variable_name] = self.variable_value

class ApplicationVersion:

    def __init__(self, version_node):
        self.title = version_node.get("title")
        self.default = version_node.get("default") == "true"
        self.commands = []

        for command_node in version_node.xpath("./*"):
            if command_node.tag == "setVariable":
                self.commands.append( SetVariable(command_node) )

    def __str__(self):
        return self.title

    def execute(self):
        for command in self.commands:
            command.execute()

class Application:

    def __init__(self, application_node):
        self.title = application_node.get("title")
        self.versions = []
        self.selected_version = None

        for version_node in application_node.xpath("./version"):
            application_version = ApplicationVersion(version_node)
            self.versions.append(  application_version )

    def select_version(self, version):
        self.selected_version = version

    def execute(self):
        if self.selected_version != None:
            self.selected_version.execute()

class Environment:

    def __init__(self, environment_node):
        self.id = environment_node.get("id")
        self.name = environment_node.get("name")
        self.applications = []

        for application_node in environment_node.xpath("./application"):
            self.applications.append(  Application(application_node) )

    def __str__(self):
        return "Environment: id:" + self.id

    def execute(self):
        for application in self.applications:
            application.execute()

class Environments:

    def __init__(self, environments_filename):
        self.environments = []
        self.selected_environment = None

        tree = etree.parse(environments_filename)
        for environment_node in tree.xpath("/environments/environment"):
            environment = Environment(environment_node)
            self.environments.append(environment)

    def select_environment(self, environment):
        self.selected_environment = environment

    def execute(self):
        if self.selected_environment != None:
            self.selected_environment.execute()

class EnvironmentSelector:

    def __init__(self):

        global public_variables
        public_variables = dict()

        self.environments = Environments(sys.argv[1])

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Hello Buttons!")
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(10)

        vbox = gtk.VBox(False, 0)
        self.window.add(vbox);

        self.notebook = gtk.Notebook()
        vbox.add(self.notebook)

        for environment in self.environments.environments:
            self.create_notebook_tab(environment)

        self.notebook.connect_object("switch-page", self.do_environment_select, None)
        self.notebook.show()

        self.ok_button = gtk.Button("OK")
        self.ok_button.connect("clicked", self.do_ok)
        self.ok_button.show()
        vbox.add(self.ok_button)
        vbox.show()

        self.cancel_button = gtk.Button("Cancel")
        self.cancel_button.connect("clicked", self.do_cancel)
        self.cancel_button.show()
        vbox.add(self.cancel_button)
        vbox.show()

        self.window.show()

    def callback(self, widget, data=None):
        print "Hello again - %s was pressed" % data

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def do_ok(self, button):
        self.environments.execute()
        for variable_name in public_variables.keys():
            print "variable " + variable_name + " = " + public_variables[variable_name]


    def do_cancel(self, button):
        print "CANCEL!";

    def do_version_selected(self, button, application, version):
        print "Version Selected", version
        application.select_version(version)

    def do_environment_select(self, notebook, page, page_num):
        self.environments.select_environment(self.environments.environments[page_num])
        print "selected environment", self.environments.selected_environment
    
    def create_notebook_tab(self, environment):

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
            radio_button_group.connect("toggled", self.do_version_selected, application, None)
            application_hbox.pack_start(radio_button_group, expand=False, padding=5)

            for version in application.versions:
                version_radiobutton = gtk.RadioButton(radio_button_group, version.title)
                version_radiobutton.show()
                version_radiobutton.connect("toggled", self.do_version_selected, application, version)
                application_hbox.pack_start(version_radiobutton, expand=False, padding=5)
                if version.default:
                    version_radiobutton.set_active(True)
            
        tab_label = gtk.Label(environment.name)
        self.notebook.append_page( tab_pane_box, tab_label=tab_label)
            
        tab_label.show()
        tab_pane_box.show()


    def main(self):
        gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    selector = EnvironmentSelector()
    selector.main()
