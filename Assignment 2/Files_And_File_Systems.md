# Files And File Systems
In order to use postgreSQL on the CS Teaching Labs (and perhaps also on your own machine), you will need to be aware of where your files are and be able to move them between your machine and the CS Teaching Labs machines. This page explains a bit about files and directories that may not be familiar to all, and then goes through different methods for moving files between machines.

## Files and Directories
We use our computers to store many types of data, such as word documents for course reports, code for programming assignments, and photos from past vacations.

The file system is responsible for managing this data, which is organized into files and directories (directories are often also called folders). Each file includes one of the types of data mentioned earlier, whereas directories can contain files or other directories.

In your file system, files and directories are organized in a tree-like structure, with the root directory, being the top-most directory.

In macOS and Linux, the root directory is denoted by /, whereas in Windows, the root directory is the drive named C:/. 

A file manager is the program that provides a user-friendly interface for browsing files and directories on your computer, and making modifications to them. 'Windows Explorer' is the default file manager on Windows, 'Finder' is the default on macOs, and 'Nautilus' is the default on Ubuntu (Linux).

Here is an example of a file system structure:

/
├── bin
├── users
│   └── marina
│       ├── Desktop
│       ├── Documents
│       └── csc343
│           ├── miscellaneous
│           │   ├── dir1
│           │   │   └── file1.py
│           │   └── dir2
│           │       └── file2.py
│           └── a2
│               ├── schema.ddl
│               ├── a2.py
│               └── q1.sql
└── tmp
At the top, we have the root directory (denoted here by /), and in it there are three things: a file called bin, a folder called users, and a file called tmp. Notice that the leaves of the tree are files, and the internal nodes are directories.

## File types
A file is an object that holds a collection of data, and is identified by a file name.

A file name usually has the format file_name.file_extension. The file extension indicates the type of the file e.g. Java files by convention have the file extension .java, and Python files have the file extension .py.


NOTE	This two-part file naming system is just a convention i.e., just replacing a .txt with a .pdf will NOT convert your file to a pdf document.
The file system doesn't require each filename to include an extension. However, this two-part system is widely followed because it communicates to the reader the type of the file without them having to even open it. Furthermore, it gives programs a hint about the contents of a file. For example, your text editor may use the filename extension to identify what programming language is used in that file, so that it can use syntax highlighting based on the rules of that language.

There are many types of files, which can be broadly classified into two broad categories:

Plain text files: These include human-readable contents. You can therefore open these files and inspect or edit their contents in a text editor (e.g., nano, vim, emacs) or an IDE (e.g., PyCharm).
Examples of this type include comma-separated values files (.csv), source code files e.g. Python files (.py) and PostgreSQL files (.sql, .ddl) and text files with artbitrary content in no particular language (.txt
Binary files: you need a special program to open these files e.g. you need a PDF viewer to see the contents of a pdf file. If you try opening one of these files using a text editor, you will see a set of weird-looking characters.
Examples of this type of files includes portable document format files (.pdf), pictures (.jpg, .png, .tiff), movies (.mp4, .mov), word documents (.docx), excel workbooks (.xlsx) and zip files (.zip).

DEFINITION	An Integrated Development Environment (IDE) is a software application that integrates many useful tools to create a convenient development environment. An editor is one of these tools. As a result, you can edit any plain-text file in an editor, but using an IDE provides you with more tools that can facilitate your programming experience.
PyCharmLinks to an external site. is a popular IDE that you might find useful (but you are free to use any IDE you prefer). 
 

## Navigating the file system in the terminal
When you open a new terminal window, your start in your root directory. You can move around within your directories. Your file system will keep track or where you currently are (your current working directory) and will show you your files from the perspective of that directory.  For example, in the above filesystem, if your current working directory is dir1, you won't be able to access file2.py.

Here are some helpful commands:

Linux/macOS	Windows
Report what is the current working directory.	>>> pwd	>>> cd
List the contents of the current working directory.	>>> ls	>>> dir
Change the current working directory, where <path> can be a relative or absolute path (see below).	>>> cd <path>	>>> cd <path>
## Path
A path is a slash-separated list of directory names, ending with a file name or a directory name, that uniquely identifies the location of a file/directory within the directory tree hierarchy. Think of it as a path through your directory tree.

Absolute path: The path of a file starting from the root e.g. in the above, the absolute file path of file2.py is /users/marina/csc343/miscellaneous/dir2/file2.py.
Relative path: The path of a file or directory relative to the current working directory. For example, if the current working directory is marina, the path to file file2.py is csc343/miscellaneous/dir2/file2.py.
When writing this type of path, we can use . to refer to the current working directory and .. to refer to the current working directory's parent directory.
We can also chain .. to refer to directories even further up the hierarchy. For example, ../../ refers to the parent directory of the current working directory's parent directory.
## Using PostgreSQL locally
You can find what you need to install PostgreSQL locally hereLinks to an external site.. 

Select your operating system.
Download the 16.10 installer (the version installed on the teach labs).
Run the installer and follow the given instructions.
You will be given the option to select a username and a password. By default, the value postgres is used for both. If you decide to change either, make sure to remember the changed values.
Once the installation is complete, you can use the psql command locally by opening a new terminal and typing the command psql -U <username> where username is the user name you selected during installation (postgres by default). You will subsequently be prompted to enter the password selected during installation. 


NOTE	If you decide to work locally on CSC343 assignments, you must ensure that your code runs on the CS Teaching Labs. Be sure to test your code on the CS Teaching Labs regularly. Code that doesn't run there will earn 0.
## Working on a remote server
We encourage you to use the CS Teaching Labs environment as your main computing environment for the SQL portion of this course.  Each student in CSC343 has an account on the Teaching Lab computers. You can find your account name and set (or reset) your password at https://www.teach.cs.toronto.edu/account.

You can access the teaching lab environment and connect to dbsrv1 remotely (without being physically in the lab) using the sshLinks to an external site., as discussed here.

Below we describe three different methods for moving files between your computer and dbsrv1. You only need to use one of these methods. Pick the way, you are most comfortable with.

Note: The following sections include links to third-party software. These links and the software associated with them are provided “as is” without warranty of any kind, and are to be used at your own risk.

### Moving files between a remote server and your computer, Method 1: Using SCP
SCP stands for secure copy and it is a command line utility that allows you to securely copy files/folders between your local machine and a remote server (dbsrv1 in this case).

Setting Up
For this demo, I created a directory on the remote server (dbsrv1): remote_dir that includes two files: file1.txt and file2.sql. I also created a directory on my local machine local_dir that includes two files: file3.txt and file4.sql. 

This section shows the steps of creating these files and directories using the command line. However, you can do the same using a file manager (e.g., file explorer on Windows, finder on macOS, Nautilus on Linux).

First, I types the following commands on dbsrv1:

dbsrv1:~$ mkdir remote_dir
dbsrv1:~$ cd remote_dir/
dbsrv1:~/remote_dir$ touch file1.txt
dbsrv1:~/remote_dir$ touch file2.sql
dbsrv1:~/remote_dir$ pwd
/u/marinat/remote_dir
The first two lines create a new directory: remote_dir and changes the current directory to that newly-created directory. I then use the command touch to create two empty files for demoing purposes. Finally, I check the full path of the current working directory using pwd (we will need that later).

Similarly, I did the following on my local machine. These commands will differ if you are using Windows.

marinat:~ marina$ mkdir local_dir
marinat:~ marina$ cd local_dir/
marinat:local_dir marina$ touch file3.txt
marinat:local_dir marina$ touch file4.sql
marinat:local_dir marina$ pwd
/Users/marina/local_dir
Doing the file transfer
Note: For all of the below commands, you can use relative paths instead of absolute paths.

Copying a local file to the remote server
To copy a file on your local machine to the remote server, you will need to type the following on your local machine:

scp <path_to_file_on_local> <user_name>@dbsrv1.teach.cs.toronto.edu:<path_to_directory_on_remote>
You will be prompted to provide your password to the remote server, before file transfer starts.

For example, to copy file3.txt from my local machine to the remote server, under the directory remote_dir, I had to issue the following command on my local machine:

marinat:~ marina$ scp /Users/marina/local_dir/file3.txt marinat@dbsrv1.teach.cs.toronto.edu:/u/marinat/remote_dir
Copying a local directory to the remote server
To copy a directory on your local machine to the remote server, you will need to type the following on your local machine:

scp -r <path_to_directory_on_local> <user_name>@dbsrv1.teach.cs.toronto.edu:<path_to_directory_on_remote>
You will be prompted to provide your password to the remote server, before file transfer starts.

For example, the following will copy remote_dir from my local machine to the remote server, under the directory remote_dir:

marinat:~ marina$ scp -r /Users/marina/local_dir/ marinat@dbsrv1.teach.cs.toronto.edu:/u/marinat/remote_dir
Copying a remote file to the local machine
To copy a file on the remote server to your local machine, you will need to type the following on your local machine:

scp <user_name>@dbsrv1.teach.cs.toronto.edu:<path_to_file_on_remote> <path_to_file_on_local>
You will be prompted to provide your password to the remote server, before file transfer starts.

For example, typing the following on my local machine will copy file2.txt from my the remote server, to my local machine under the directory local_dir: 

marinat:~ marina$ scp  marinat@dbsrv1.teach.cs.toronto.edu:/u/marinat/remote_dir/file1.txt /Users/marina/local_dir/
Copying a remote directory to the local machine
To copy a directory on the remote server to your local machine, you will need to type the following on your local machine:

scp -r <user_name>@dbsrv1.teach.cs.toronto.edu:<path_to_directory_on_remote> <path_to_file_on_local>
For example, typing the following on my local machine will copy remote_dir from my the remote server, to my local machine under the directory local_dir: 

marinat:~ marina$ scp -r marinat@dbsrv1.teach.cs.toronto.edu:/u/marinat/remote_dir /Users/marina/local_dir/
Using SCP on Linux or macOS
The SCP utility is included in most Linux and macOS distributions and so you wouldn't need to install anything in this case. Follow the above instructions to move files and folders between your local machine and remote server.

Using SCP on Windows
Windows machines don't come pre-installed with scp. Instead, you will need to install PSCP. You can do that by installing Putty, which includes PSCP. Alternatively, you can download PSCP only (from the same page).

You can still follow the above steps but you will need to replace scp to pscp.

 

### Moving files between a remote server and your computer, Method 2: Mounting the remote file system
Another option to transfer files easily between your local machine and a remote server is to mount the remote filesystem onto your local file system. As a result your local file system "sees" the remote file system as part of itself.

sshfs is available on Linux and macOs and can be used as follows to mount a remote directory onto the local filesystem:

sshfs <user_name>@dbsrv1.teach.cs.toronto.edu:<path_to_remote_directory> <path_to_local_directory>
For example, I can do the following to mount my home directory on the remote server /u/marinat/ onto my local filesystem under the local directory Remote.

marinat:~ marina$ sshfs marinat@dbsrv1.teach.cs.toronto.edu:/u/marinat/ /Users/marina/Remote
Note that you need the final forward slash after the name of the remote directory.

I was then prompted to enter my password. Now, if I change into the Remote directory, I will see all files on my remote home directory and will be able to make edits as necessary.

It is advisable to unmount the directory once you are done your edits and you can do that by using the command:

umount <path_to_local_directory>
For example, using the above example, I will need to type:

umount Remote
### Moving files between a remote server and your computer, Method 3: Using an SFTP client
You can also use an application that allows the secure transfer of files. Two examples of such application are cyberduck and mountain duck. Both are freely available for download on Windows and macOs. 

 