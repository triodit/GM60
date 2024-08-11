import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports

class GM60BarcodeReader:
    def __init__(self, master):
        self.master = master
        self.master.title("GM60 Barcode Reader Configuration")
        
        # Serial connection
        self.ser = None
        
        # Frame for COM Port selection
        self.port_frame = ttk.LabelFrame(self.master, text="COM Port Selection")
        self.port_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ttk.Label(self.port_frame, text="Select COM Port:").grid(row=0, column=0, padx=5, pady=5)
        self.combobox = ttk.Combobox(self.port_frame, values=self.get_serial_ports(), state="readonly")
        self.combobox.grid(row=0, column=1, padx=5, pady=5)
        
        self.connect_button = ttk.Button(self.port_frame, text="Connect", command=self.connect_port)
        self.connect_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Frame for current state
        self.state_frame = ttk.LabelFrame(self.master, text="Current State")
        self.state_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        ttk.Label(self.state_frame, text="Current Read Mode:").grid(row=0, column=0, padx=5, pady=5)
        self.read_mode_label = ttk.Label(self.state_frame, text="N/A")
        self.read_mode_label.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.state_frame, text="Current Baud Rate:").grid(row=1, column=0, padx=5, pady=5)
        self.baud_rate_label = ttk.Label(self.state_frame, text="N/A")
        self.baud_rate_label.grid(row=1, column=1, padx=5, pady=5)
        
        # Frame for configuration
        self.config_frame = ttk.LabelFrame(self.master, text="Configuration")
        self.config_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        # Read Mode Configuration
        ttk.Label(self.config_frame, text="Set Read Mode:").grid(row=0, column=0, padx=5, pady=5)
        self.read_mode_combobox = ttk.Combobox(self.config_frame, values=["Continuous Mode", "Induction Mode"], state="readonly")
        self.read_mode_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Baud Rate Configuration
        ttk.Label(self.config_frame, text="Set Baud Rate:").grid(row=1, column=0, padx=5, pady=5)
        self.baud_rate_combobox = ttk.Combobox(self.config_frame, values=["9600", "19200", "38400", "57600", "115200"], state="readonly")
        self.baud_rate_combobox.grid(row=1, column=1, padx=5, pady=5)

        # LED Configuration
        ttk.Label(self.config_frame, text="Set LED Mode:").grid(row=2, column=0, padx=5, pady=5)
        self.led_mode_combobox = ttk.Combobox(self.config_frame, values=["Normal", "Normally On", "Off"], state="readonly")
        self.led_mode_combobox.grid(row=2, column=1, padx=5, pady=5)

        # LED Brightness Configuration
        ttk.Label(self.config_frame, text="Set LED Brightness:").grid(row=3, column=0, padx=5, pady=5)
        self.led_brightness_combobox = ttk.Combobox(self.config_frame, values=["Low", "Middle", "High"], state="readonly")
        self.led_brightness_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Set Configuration Button
        self.set_button = ttk.Button(self.config_frame, text="Set Configuration", command=self.set_configuration)
        self.set_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
    def get_serial_ports(self):
        """Returns a list of available COM ports."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect_port(self):
        """Connect to the selected COM port."""
        selected_port = self.combobox.get()
        if selected_port:
            try:
                self.ser = serial.Serial(selected_port, 57600, timeout=1)  # 57600 is the default baud rate
                self.update_current_state()
            except serial.SerialException as e:
                messagebox.showerror("Connection Error", f"Failed to connect to {selected_port}\n{e}")
                self.ser = None
    
    def send_command(self, command):
        """Send command to the barcode reader and return the response."""
        try:
            self.ser.write((command + '\r\n').encode())
            response = self.ser.read(100).decode().strip()
            return response
        except Exception as e:
            messagebox.showerror("Communication Error", f"Failed to send command: {e}")
            return ""

    def update_current_state(self):
        """Retrieve and display the current state of the device."""
        # Placeholder for the actual command to get the read mode
        read_mode = self.send_command("VAL1?")  # Replace with the correct command to get the current read mode
        if read_mode == "02":
            self.read_mode_label.config(text="Continuous Mode")
        elif read_mode == "03":
            self.read_mode_label.config(text="Induction Mode")
        else:
            self.read_mode_label.config(text="Unknown Mode")
        
        # Placeholder for the actual command to get the baud rate
        baud_rate = self.send_command("BAUD?")  # Replace with the correct command to get the current baud rate
        baud_rate_mapping = {
            "9600": "9600",
            "19200": "19200",
            "38400": "38400",
            "57600": "57600",
            "115200": "115200"
        }
        self.baud_rate_label.config(text=baud_rate_mapping.get(baud_rate, "Unknown Baud Rate"))
    
    def set_configuration(self):
        """Set the configuration based on the dropdown selections."""
        selected_mode = self.read_mode_combobox.get()
        selected_baud_rate = self.baud_rate_combobox.get()
        selected_led_mode = self.led_mode_combobox.get()
        selected_led_brightness = self.led_brightness_combobox.get()
        
        if selected_mode == "Continuous Mode":
            mode_command = "SET 02"  # Replace with the correct command for Continuous Mode
        elif selected_mode == "Induction Mode":
            mode_command = "SET 03"  # Replace with the correct command for Induction Mode
        else:
            messagebox.showerror("Configuration Error", "Invalid mode selected.")
            return

        if selected_baud_rate:
            baud_command = f"SET BAUD {selected_baud_rate}"  # Replace with the correct command to set baud rate

        if selected_led_mode == "Normal":
            led_command = "SET LED 01"  # Replace with the correct command for Normal LED mode
        elif selected_led_mode == "Normally On":
            led_command = "SET LED 02"  # Replace with the correct command for Normally On LED mode
        elif selected_led_mode == "Off":
            led_command = "SET LED 00"  # Replace with the correct command to turn off LED
        else:
            messagebox.showerror("Configuration Error", "Invalid LED mode selected.")
            return

        if selected_led_brightness == "Low":
            brightness_command = "SET BRIGHT 01"  # Replace with the correct command for Low brightness
        elif selected_led_brightness == "Middle":
            brightness_command = "SET BRIGHT 50"  # Replace with the correct command for Middle brightness
        elif selected_led_brightness == "High":
            brightness_command = "SET BRIGHT 99"  # Replace with the correct command for High brightness
        else:
            messagebox.showerror("Configuration Error", "Invalid LED brightness selected.")
            return

        # Send commands
        self.send_command(mode_command)
        self.send_command(baud_command)
        self.send_command(led_command)
        self.send_command(brightness_command)
        
        messagebox.showinfo("Configuration", "Configuration set successfully.")
        self.update_current_state()
    
    def close(self):
        if self.ser:
            self.ser.close()
        self.master.quit()

# Main application
root = tk.Tk()
app = GM60BarcodeReader(root)
root.protocol("WM_DELETE_WINDOW", app.close)
root.mainloop()
