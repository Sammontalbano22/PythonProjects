#Purpose: Creates a file system tree
#File Name:Sam shellterminal.py
#Date: 6/5/24
#Course: COMP1353
#Assignment: A Simple Shell
#Collaborators:Jonah Perlman
#Internet Sources: None


from __future__ import annotations
import pickle

class TreeNode:  # TreeNode class allows nodes to be made for the directory
    def __init__(self, name, parent: TreeNode, is_directory):
        self.name = name
        self.parent = parent
        self.children = []
        self.is_directory = is_directory
    
    def append_child(self, name, is_directory):
        new_child = TreeNode(name, self, is_directory)
        self.children.append(new_child)
    
    def __str__(self):
        if self.is_directory:
            return f"{self.name} <directory>"
        else:
            return self.name
    
    def is_root(self):
        return self.parent is None
        
class FileSystem:
    def __init__(self):
        self.root = TreeNode('/', None, True)
        self.current_directory = self.root
    
    def cd(self, name):
        if name == '..':  # makes the directory change to the parent of the current directory
            if self.current_directory.parent is not None:
                self.current_directory = self.current_directory.parent
        else:  # if the user does not input "..", then the directory changes to the name that the user inputs
            for node in self.current_directory.children:
                if node.name == name and node.is_directory:
                    self.current_directory = node
                    return
            raise ValueError(f"No such directory: {name}")
        
    def tree(self):
        print("Tree:")
        self._tree_helper(self.root, 0)  # Calls the helper method on the root directory
    
    def _tree_helper(self, node, level):  # prints out all of the nodes above the current directory (ancestors)
        print('    ' * level + str(node))
        for child in node.children:
            self._tree_helper(child, level + 1)
    
    def ls(self):  # shows the children of the current directory, which are just the contents of the folder
        for child in self.current_directory.children:
            print(child)
    
    def mkdir(self, dirname):  # creates a new directory 
        self.check_make_file(dirname)
        self.current_directory.append_child(dirname, True)
    
    def check_make_file(self, name):  # checks to see if the file or directory that was made does not already exist
        for child in self.current_directory.children:
            if child.name == name:
                raise NameError("That file or directory already exists")
    
    def touch(self, name):  # makes a new file
        self.check_make_file(name)
        self.current_directory.append_child(name, False)
    
    def rm(self, filename):  # removes files
        for child in self.current_directory.children:
            if child.name == filename and not child.is_directory:
                self.current_directory.children.remove(child)
                return
        raise ValueError("Files only can be removed using the rm function!")

    def rmdir(self, dirname):  # removes directories
        for child in self.current_directory.children:
            if child.name == dirname and child.is_directory:
                if not child.children:  # Ensure directory is empty
                    self.current_directory.children.remove(child)
                    return
                else:
                    raise ValueError("Directory is not empty!")
        raise ValueError("No such directory or it is not a directory!")
    
    def pwd(self):  # prints the path that the user has taken to get to their node
        path = ""
        current_node = self.current_directory
        while current_node.parent is not None:
            path = f"/{current_node.name}" + path
            current_node = current_node.parent
        return path


def user_input(file_system):
    while True: 
        print("\nCurrent Directory:", file_system.current_directory.name)  # all of these explain what the possible commands are to the user
        print("ls: lists contents of current directory")
        print("tree: Print the tree structure")
        print("mkdir <directory_name>: creates directory")
        print("cd <directory_name>: change directory")
        print("touch <file_name>: create a file")
        print("rm: <file_name>: remove a file")
        print("rmdir <directory_name>: remove directory")
        print(" ..: If you want to go back one directory")
        print("pwd: prints the working directory")
        print("exit: Save and exit")
        
        user_input = input("Enter command: ").split()
        if not user_input:
            continue
        command = user_input[0]
        
        # the code below runs through every possible input the user could give, and takes user to output before relooping
        if command == 'ls':
            file_system.ls()
        elif command == 'tree':
            file_system.tree()
        elif command == 'mkdir':
            try:
                dirname = user_input[1]
                file_system.mkdir(dirname)
            except IndexError:
                print("Please provide a directory name.")
            except ValueError as e:
                print(e)
        elif command == 'cd':
            try:
                dirname = user_input[1]
                file_system.cd(dirname)
            except IndexError:
                print("Please provide a directory name.")
            except ValueError as e:
                print(e)
        elif command == 'touch':
            try:
                filename = user_input[1]
                file_system.touch(filename)
            except IndexError:
                print("Please provide a file name.")
            except ValueError as e:
                print(f'Content: {e}')
        elif command == 'rm':
            try:
                filename = user_input[1]
                file_system.rm(filename)
            except IndexError:
                print("Please provide a file name.")
            except ValueError as e:
                print(e)
        elif command == 'rmdir':
            try:
                dirname = user_input[1]
                file_system.rmdir(dirname)
            except IndexError:
                print("Please provide a directory name.")
            except ValueError as e:
                print(e)
        elif command == 'pwd':
            print("Current Directory Path:", file_system.pwd())
        elif command == 'exit':
            return file_system
        else:
            print("Invalid command.")
    

def main():
    file_system = FileSystem()
    user_input(file_system)


def _main_with_pickle():
    ##pickle save info !
    try:
        with open("file_system_testing.bin", "rb") as file_source:
            file_system = pickle.load(file_source)
            print("File System loaded")
    except:
        print("Creating a new file system: file doesn't exist or data file is out of date because FileSystem class changed")
        file_system = FileSystem()
        
    file_system = user_input(file_system)
    
    with open("file_system_testing.bin", "wb") as file_destination:
        pickle.dump(file_system, file_destination)
        print("File system saved")
    

if __name__ == '__main__':

    _main_with_pickle()

