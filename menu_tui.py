import urwid
import platform
import os
import psutil  # For system stats
import socket  # For getting local IP address
import requests  # For fetching WAN (public) IP address

# Function to get system info, including disk, memory, and network (IP addresses)
def get_sys_info():
    try:
        with open("/etc/fedora-release") as f:
            fedora_version = f.read().strip()
    except FileNotFoundError:
        fedora_version = "Fedora version not found"
    
    kernel_version = platform.uname().release
    architecture = platform.machine()
    
    try:
        cpu_model = platform.processor() or "Unknown CPU"
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_info = f"{cpu_model} | Usage: {cpu_usage}%"
    except Exception as e:
        cpu_info = f"CPU Info not available: {e}"
    
    disk = psutil.disk_usage('/')
    total_disk = round(disk.total / (1024 ** 3), 2)
    used_disk = round(disk.used / (1024 ** 3), 2)
    free_disk = round(disk.free / (1024 ** 3), 2)

    memory = psutil.virtual_memory()
    total_memory = round(memory.total / (1024 ** 3), 2)
    used_memory = round(memory.used / (1024 ** 3), 2)
    free_memory = round(memory.available / (1024 ** 3), 2)

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    try:
        public_ip = requests.get('https://api.ipify.org').text
    except requests.RequestException:
        public_ip = "Unable to fetch public IP"

    return (f"System Info: {fedora_version} | Kernel: {kernel_version} | Arch: {architecture} | CPU: {cpu_info}\n"
            f"Disk: {used_disk}/{total_disk} GB used, {free_disk} GB free | "
            f"Memory: {used_memory}/{total_memory} GB used, {free_memory} GB free\n"
            f"Local IP: {local_ip} | WAN IP: {public_ip}")

# Function to update the system (for Option 1)
def update_system(button):
    response.set_text("Updating the system... Please wait.")
    os.system("sudo dnf update -y")
    response.set_text("System update complete!")

# Create an updated Synthwave color palette with valid urwid colors
palette = [
    ('reversed', 'standout', ''),
    ('menu', 'light magenta', 'dark blue'),
    ('check', 'light cyan', 'dark magenta'),
    ('bg', 'light cyan', 'black'),
    ('header', 'dark gray', 'dark cyan'),
    ('header_standout', 'dark gray,standout', 'dark cyan'),
    ('highlight', 'yellow', 'dark blue'),
    ('selected', 'light cyan', 'dark magenta'),
    ('button', 'yellow', 'dark magenta'),
    ('button_focus', 'light cyan', 'dark red'),
    ('divider', 'dark gray', 'light cyan'),
    ('description', 'light green', 'dark blue'),
]

# Mapping of menus based on category
menus = {
    'System Setup': ["Update System", "Manage Disk", "Manage Users"],
    'Applications Setup': ["Install Apps", "Remove Apps", "Manage Repositories"],
    'Security': ["Firewall", "SELinux", "Antivirus"],
    'Utilities': ["Network Tools", "Backup", "Monitor"],
    'Extra': ["Themes", "Fonts", "Accessibility"]
}

# Function to create a dynamic checklist based on the selected category
def create_checklist(category):
    software = menus.get(category, [])
    checkboxes = [urwid.AttrMap(urwid.CheckBox(item), 'check', focus_map='reversed') for item in software]
    return urwid.ListBox(urwid.SimpleFocusListWalker(checkboxes))

# Function to handle menu selection
def menu_selected(button, category):
    global right_checklist  # To modify the right panel dynamically

    # Create a new checklist for the selected category
    new_checklist = urwid.BoxAdapter(urwid.AttrMap(create_checklist(category), 'bg'), height=10)
    
    # Update the right panel with the new checklist
    right_checklist.original_widget = new_checklist
    
    # Update the description text to show the selected category
    description.base_widget.set_text(f"Showing menu for {category}")

# Quit function
def quit_program(button):
    raise urwid.ExitMainLoop()

# Left Menu categories
menu_categories = ['System Setup', 'Applications Setup', 'Security', 'Utilities', 'Extra']

# Create the menu layout with a Quit button at the bottom
def create_menu_layout():
    menu_body = []
    for category in menu_categories:
        button = urwid.Button(category)
        urwid.connect_signal(button, 'click', menu_selected, user_args=[category])
        menu_body.append(urwid.AttrMap(button, 'menu', focus_map='reversed'))
    
    menu_listbox = urwid.ListBox(urwid.SimpleFocusListWalker(menu_body))
    quit_button = urwid.Button("Quit", quit_program)
    
    return urwid.Pile([
        urwid.BoxAdapter(menu_listbox, height=len(menu_categories)),
        urwid.Divider(),
        urwid.AttrMap(quit_button, 'button')
    ])

# Create layout
left_menu = urwid.Filler(create_menu_layout(), valign='top')
right_checklist = urwid.AttrMap(urwid.BoxAdapter(create_checklist('System Setup'), height=10), 'bg')

# Create header with system info
sys_info_text = urwid.Text(get_sys_info(), align='center')
header = urwid.AttrMap(urwid.Filler(sys_info_text, valign='middle'), 'header_standout')

# Create the description box with a border and style
description = urwid.AttrMap(urwid.Text(u"Select a menu category on the left."), 'description')
description_box = urwid.LineBox(description)

# **Define the response text box (fixes the error)**
response = urwid.Text(u"")  # Initialize the response box to show feedback

# Main layout using Pile and Columns
main_layout = urwid.Pile([
    (5, header),
    urwid.Filler(urwid.Columns([
        (20, left_menu),
        right_checklist
    ], dividechars=1), valign='top'),
    (8, description_box),
    urwid.Filler(response, valign='bottom')  # Display the response at the bottom
])

# Run the UI loop
urwid.MainLoop(main_layout, palette).run()
