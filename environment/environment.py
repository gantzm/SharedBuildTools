#!/usr/bin/python

from lxml import etree
import Tkinter as tk
import sys


class SettingOption:
    
    def __init__(self, option_node):
        self.title = option_node.get("title")
        self.default = option_node.get("default") == "true"
        self.value = option_node.text

    def __str__(self):
        return "SettingOption: Title:" + self.title + ", Default:" + str(self.default) + ", Value:" + self.value
    
class Setting:

    def __init__(self, setting_node, tkInstance):
        self.title = setting_node.get("title")
        self.name = setting_node.get("name")
        self.rbValue = tk.StringVar(tkInstance)
        self.options = []

        for option in setting_node.xpath("./option"):
            settingOption = SettingOption(option)
            self.options.append(settingOption)

    def __str__(self):
        return "Setting: Title:" + self.title + " Name:" + self.name + " Value:" + self.rbValue.get()

    def write(self, f):
        f.write(self.name + "=" + self.rbValue.get() + "\n")

class Environment:

    def __init__(self, master, environment_node):
        self.settings = dict()
        self.id = environment_node.get("id")
        self.name = environment_node.get("name")
        self.settings = []

        for setting in environment_node.xpath("./setting"):
            envSetting = Setting(setting, master)
            self.settings.append(envSetting)

    def __str__(self):
        return "Environment: ID:" + self.id + " Name:" + self.name

    def do_output(self, output_file_name):
        f = open(output_file_name, "w")
        for setting in self.settings:
            setting.write(f)
        f.close()

class Environments:

    def __init__(self, master, filename):
        self.environments = dict()

        tree = etree.parse(filename)
        envNode = tree.xpath("/environments/environment")

        for environmentXml in envNode:
            environment = Environment(master, environmentXml)
            self.environments[environment.id] = environment

    def __str__(self):
        return "Environments:"

    def find(self, id):
        return self.environments[id];

class App:

    def __init__(self, master):
        
        self.frame = tk.Frame(master)
        self.frame.grid(padx=15, pady=15)

        self.environments = Environments(master, sys.argv[1] )
        self.environment = self.environments.find( sys.argv[2] )
        
        currentRow = 0
        for setting in self.environment.settings:

            settingLabel = tk.Label(self.frame, text=setting.title)
            settingLabel.grid(row=currentRow, sticky=tk.W)
            currentRow += 1

            for option in setting.options:

                rb = tk.Radiobutton(self.frame, text=option.title, variable=setting.rbValue, value=option.value)
                rb.grid(row=currentRow, sticky=tk.W, padx=15)
                currentRow += 1
                rb.deselect()

                if option.default:
                    rb.select()

        self.cancel_button = tk.Button(self.frame, text="Cancel", command=self.frame.quit)
        self.cancel_button.grid(row=currentRow)
        currentRow += 1

        self.ok_button = tk.Button(self.frame, text="OK", command=self.do_ok)
        self.ok_button.grid(row=currentRow)
        currentRow += 1

    def do_ok(self):
        self.environment.do_output(sys.argv[3])
        self.frame.quit()
        

root = tk.Tk()

app = App(root)

root.mainloop()
