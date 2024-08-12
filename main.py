import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import time

class GM60BarcodeReader:
    def __init__(self, master):
        self.master = master
        self.master.title("GM60 Barcode Reader Configuration")
        
        # Serial connection
        self.ser = None
        self.baud_rates = ["9600", "1200", "4800", "14400", "19200", "38400", "57600", "115200"]

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
        
        # Current Read Mode
        ttk.Label(self.state_frame, text="Current Read Mode:").grid(row=0, column=0, padx=5, pady=5)
        self.read_mode_label = ttk.Label(self.state_frame, text="N/A")
        self.read_mode_label.grid(row=0, column=1, padx=5, pady=5)

        # Current Baud Rate
        ttk.Label(self.state_frame, text="Current Baud Rate:").grid(row=1, column=0, padx=5, pady=5)
        self.baud_rate_label = ttk.Label(self.state_frame, text="N/A")
        self.baud_rate_label.grid(row=1, column=1, padx=5, pady=5)

        # Current LED Mode
        ttk.Label(self.state_frame, text="Current LED Mode:").grid(row=2, column=0, padx=5, pady=5)
        self.led_mode_label = ttk.Label(self.state_frame, text="N/A")
        self.led_mode_label.grid(row=2, column=1, padx=5, pady=5)

        # Current LED Brightness
        ttk.Label(self.state_frame, text="Current LED Brightness:").grid(row=3, column=0, padx=5, pady=5)
        self.led_brightness_label = ttk.Label(self.state_frame, text="N/A")
        self.led_brightness_label.grid(row=3, column=1, padx=5, pady=5)

        # Current Color Mode
        ttk.Label(self.state_frame, text="Current Color Mode:").grid(row=4, column=0, padx=5, pady=5)
        self.color_mode_label = ttk.Label(self.state_frame, text="N/A")
        self.color_mode_label.grid(row=4, column=1, padx=5, pady=5)

        # Read Button to update the current state
        self.read_button = ttk.Button(self.state_frame, text="Read", command=self.update_current_state)
        self.read_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
        # Frame for configuration
        self.config_frame = ttk.LabelFrame(self.master, text="Configuration")
        self.config_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        # Read Mode Configuration
        ttk.Label(self.config_frame, text="Set Read Mode:").grid(row=0, column=0, padx=5, pady=5)
        self.read_mode_combobox = ttk.Combobox(self.config_frame, values=["Continuous Mode", "Induction Mode"], state="readonly")
        self.read_mode_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Baud Rate Configuration
        ttk.Label(self.config_frame, text="Set Baud Rate:").grid(row=1, column=0, padx=5, pady=5)
        self.baud_rate_combobox = ttk.Combobox(self.config_frame, values=self.baud_rates, state="readonly")
        self.baud_rate_combobox.grid(row=1, column=1, padx=5, pady=5)

        # LED Mode Configuration
        ttk.Label(self.config_frame, text="Set LED Mode:").grid(row=2, column=0, padx=5, pady=5)
        self.led_mode_combobox = ttk.Combobox(self.config_frame, values=["Breathing Lamp", "Decoding Successful Prompt Light"], state="readonly")
        self.led_mode_combobox.grid(row=2, column=1, padx=5, pady=5)

        # LED Brightness Configuration
        ttk.Label(self.config_frame, text="Set LED Brightness:").grid(row=3, column=0, padx=5, pady=5)
        self.led_brightness_combobox = ttk.Combobox(self.config_frame, values=["Low", "Middle", "High"], state="readonly")
        self.led_brightness_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Color Mode Configuration
        ttk.Label(self.config_frame, text="Set Color Mode:").grid(row=4, column=0, padx=5, pady=5)
        self.color_mode_combobox = ttk.Combobox(self.config_frame, values=["Red", "Green", "Blue"], state="readonly")
        self.color_mode_combobox.grid(row=4, column=1, padx=5, pady=5)

        # Set Configuration Button
        self.set_button = ttk.Button(self.config_frame, text="Set Configuration", command=self.set_configuration)
        self.set_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
    def get_serial_ports(self):
        """Returns a list of available COM ports."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect_port(self):
        """Connect to the selected COM port and try different baud rates."""
        selected_port = self.combobox.get()
        if not selected_port:
            messagebox.showerror("Connection Error", "No COM port selected.")
            return

        for baud_rate in self.baud_rates:
            try:
                self.ser = serial.Serial(selected_port, int(baud_rate), timeout=2)  # Increased timeout
                time.sleep(1)  # Add a short delay to ensure the device is ready
                if self.test_connection():
                    self.baud_rate_label.config(text=baud_rate)
                    messagebox.showinfo("Connection Success", f"Connected successfully at {baud_rate} baud.")
                    self.update_current_state()
                    return
            except serial.SerialException as e:
                continue

        messagebox.showerror("Connection Error", "Failed to connect to the device. Please check the connection and try again.")
        self.ser = None

    def test_connection(self):
        """Test the connection by sending a command and checking the response."""
        read_mode_command = bytes([0x7E, 0x00, 0x07, 0x01, 0x00, 0x0A, 0x01, 0xEE, 0x8A])
        response = self.send_command(read_mode_command)
        return len(response) > 0  # Valid if any response is received

    def send_command(self, command_bytes):
        """Send command to the barcode reader and return the response."""
        try:
            self.ser.write(command_bytes)
            response = self.ser.read(100)
            return response
        except Exception as e:
            messagebox.showerror("Communication Error", f"Failed to send command: {e}")
            return b""

    def update_current_state(self):
        """Retrieve and display the current state of the device."""
        # Example command to get read mode (replace with actual command as needed)
        read_mode_command = bytes([0x7E, 0x00, 0x07, 0x01, 0x00, 0x0A, 0x01, 0xEE, 0x8A])
        read_mode_response = self.send_command(read_mode_command)

        # Check response and update the read mode label accordingly
        if read_mode_response:
            if read_mode_response[4] == 0x3E:
                self.read_mode_label.config(text="Continuous Mode")
            elif read_mode_response[4] == 0x3F:
                self.read_mode_label.config(text="Induction Mode")
            else:
                self.read_mode_label.config(text="Unknown Mode")
        
        # Example command to get baud rate (replace with actual command as needed)
        baud_rate_command = bytes([0x7E, 0x00, 0x07, 0x01, 0x00, 0x0A, 0x02, 0xEE, 0x8B])
        baud_rate_response = self.send_command(baud_rate_command)

        if baud_rate_response:
            baud_rate_mapping = {
                0xA0: "1200",
                0xA1: "4800",
                0xA2: "9600",
                # Add more mappings as needed
            }
            self.baud_rate_label.config(text=baud_rate_mapping.get(baud_rate_response[4], "Unknown Baud Rate"))

        # Example command to get LED mode (replace with actual command as needed)
        led_mode_command = bytes([0x7E, 0x00, 0x07, 0x01, 0x00, 0x0A, 0x03, 0xEE, 0x8C])
        led_mode_response = self.send_command(led_mode_command)

        if led_mode_response:
            led_mode_mapping = {
                0xB0: "Breathing Lamp",
                0xB1: "Decoding Successful Prompt Light",
            }
            self.led_mode_label.config(text=led_mode_mapping.get(led_mode_response[4], "Unknown LED Mode"))

        # Example command to get LED brightness (replace with actual command as needed)
        led_brightness_command = bytes([0x7E, 0x00, 0x07, 0x01, 0x00, 0x0A, 0x04, 0xEE, 0x8D])
        led_brightness_response = self.send_command(led_brightness_command)

        if led_brightness_response:
            led_brightness_mapping = {
                0xC0: "Low",
                0xC1: "Middle",
                0xC2: "High",
            }
            self.led_brightness_label.config(text=led_brightness_mapping.get(led_brightness_response[4], "Unknown LED Brightness"))

        # Example command to get color mode (replace with actual command as needed)
        color_mode_command = bytes([0x7E, 0x00, 0x07, 0x01, 0x00, 0x0A, 0x05, 0xEE, 0x8E])
        color_mode_response = self.send_command(color_mode_command)

        if color_mode_response:
            color_mode_mapping = {
                0xD0: "Red",
                0xD1: "Green",
                0xD2: "Blue",
            }
            self.color_mode_label.config(text=color_mode_mapping.get(color_mode_response[4], "Unknown Color Mode"))
    
    def set_configuration(self):
        """Set the configuration based on the dropdown selections."""
        selected_mode = self.read_mode_combobox.get()
        selected_baud_rate = self.baud_rate_combobox.get()
        selected_led_mode = self.led_mode_combobox.get()
        selected_led_brightness = self.led_brightness_combobox.get()
        selected_color_mode = self.color_mode_combobox.get()
        
        # Set Read Mode
        if selected_mode == "Continuous Mode":
            mode_command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x01, 0x00])
        elif selected_mode == "Induction Mode":
            mode_command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x01, 0x01])
        else:
            messagebox.showerror("Configuration Error", "Invalid mode selected.")
            return

        # Set Baud Rate
        baud_rate_commands = {
            "1200": bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x02, 0x00]),
            "4800": bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x02, 0x01]),
            "9600": bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x02, 0x02]),
            # Add more as needed
        }
        baud_command = baud_rate_commands.get(selected_baud_rate)

        # Set LED Mode
        if selected_led_mode == "Breathing Lamp":
            led_command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x03, 0x00])
        elif selected_led_mode == "Decoding Successful Prompt Light":
            led_command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x03, 0x01])
        else:
            messagebox.showerror("Configuration Error", "Invalid LED mode selected.")
            return

        # Set LED Brightness
        brightness_commands = {
            "Low": bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x04, 0x00]),
            "Middle": bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x04, 0x01]),
            "High": bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x04, 0x02]),
        }
        brightness_command = brightness_commands.get(selected_led_brightness)

        # Set Color Mode
        color_commands = {
            "Red": bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x05, 0x00]),
            "Green": bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x05, 0x01]),
            "Blue": bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, 0x05, 0x02]),
        }
        color_command = color_commands.get(selected_color_mode)

        # Send commands
        self.send_command(mode_command)
        self.send_command(baud_command)
        self.send_command(led_command)
        self.send_command(brightness_command)
        self.send_command(color_command)
        
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
