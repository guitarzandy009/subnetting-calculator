"""Tkinter GUI for the subnetting calculator."""

import tkinter as tk
from tkinter import ttk

from subnetcalc.core import subnet_summary


def calculate():
    """Read the CIDR from the entry field, compute the subnet summary,
    and display the result (or an error message) in the results label."""
    cidr = cidr_entry.get()

    try:
        summary = subnet_summary(cidr)
    except ValueError as e:
        result_text.set(f"Error: {e}")
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


def main():
    """Build and run the subnetting calculator GUI window."""
    global cidr_entry, result_text

    root = tk.Tk()
    root.title("Subnetting Calculator")

    cidr_label = ttk.Label(root, text="Enter CIDR (e.g. 192.168.1.0/24):")
    cidr_label.pack(padx=10, pady=(10, 0))

    cidr_entry = ttk.Entry(root, width=30)
    cidr_entry.pack(padx=10, pady=5)

    calculate_button = ttk.Button(root, text="Calculate", command=calculate)
    calculate_button.pack(padx=10, pady=5)

    result_text = tk.StringVar()
    result_label = ttk.Label(root, textvariable=result_text, justify="left", font=("Courier", 10))
    result_label.pack(padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()