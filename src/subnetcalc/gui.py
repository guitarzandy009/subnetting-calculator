"""Tkinter GUI for the subnetting calculator."""

import tkinter as tk
from tkinter import ttk

from subnetcalc.core import subnet_summary

BG_COLOR = "#1e1e2e"
FG_COLOR = "#cdd6f4"
ACCENT_COLOR = "#89b4fa"
ERROR_COLOR = "#f38ba8"
FONT_LABEL = ("Segoe UI", 11)
FONT_MONO = ("Consolas", 11)
FONT_HEADING = ("Segoe UI", 14, "bold")


def calculate():
    """Read the CIDR from the entry field, compute the subnet summary,
    and display the result (or an error message) in the results label."""
    cidr = cidr_entry.get()

    try:
        summary = subnet_summary(cidr)
    except ValueError as e:
        result_text.set(f"Error: {e}")
        result_label.configure(foreground=ERROR_COLOR)
        return

    if summary["first_usable"] is not None:
        host_range = f"{summary['first_usable']} - {summary['last_usable']}"
    else:
        host_range = "N/A (no usable hosts at this prefix)"

    output = (
        f"IP address:        {summary['ip_address']}\n"
        f"Prefix length:      /{summary['prefix_length']}\n"
        f"Subnet mask:        {summary['subnet_mask']}\n"
        f"Network address:    {summary['network_address']}\n"
        f"Broadcast address:  {summary['broadcast_address']}\n"
        f"Usable host range:  {host_range}\n"
        f"Usable host count:  {summary['usable_host_count']}"
    )
    result_text.set(output)
    result_label.configure(foreground=FG_COLOR)


def main():
    """Build and run the subnetting calculator GUI window."""
    global cidr_entry, result_text, result_label

    root = tk.Tk()
    root.title("Subnetting Calculator")
    root.configure(background=BG_COLOR)
    root.geometry("600x450")
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TFrame", background=BG_COLOR)
    style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=FONT_LABEL)
    style.configure("Heading.TLabel", background=BG_COLOR, foreground=ACCENT_COLOR, font=FONT_HEADING)
    style.configure("TEntry", fieldbackground="#313244", foreground=FG_COLOR, insertcolor=FG_COLOR)
    style.configure("TButton", background=ACCENT_COLOR, foreground=BG_COLOR, font=FONT_LABEL, padding=6)
    style.map("TButton", background=[("active", "#74a8f5")])

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid(row=0, column=0)

    heading = ttk.Label(main_frame, text="Subnetting Calculator", style="Heading.TLabel")
    heading.grid(row=0, column=0, columnspan=2, pady=(0, 15))

    cidr_label = ttk.Label(main_frame, text="CIDR:")
    cidr_label.grid(row=1, column=0, sticky="w", pady=5)

    cidr_entry = ttk.Entry(main_frame, width=25, font=FONT_MONO)
    cidr_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
    cidr_entry.insert(0, "192.168.1.0/24")

    calculate_button = ttk.Button(main_frame, text="Calculate", command=calculate)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=15)

    result_text = tk.StringVar()
    result_label = ttk.Label(
        main_frame,
        textvariable=result_text,
        justify="left",
        font=FONT_MONO,
        background="#181825",
        padding=15,
    )
    result_label.grid(row=3, column=0, columnspan=2, sticky="ew")

    root.mainloop()


if __name__ == "__main__":
    main()