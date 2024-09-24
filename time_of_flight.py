import time
from two_tone_receive import two_tone_receive  # Import the flowgraph as a module

def run_transceiver_two_tone(tb):
    """Run the transceiver two-tone flowgraph."""
    print("Running transceiver two-tone flowgraph...")
    tb.start()

def check_probe_output(tb):
    """Check the output from the probe to detect tones."""
    try:
        # Get the value from the probe (0 or 1 based on detection)
        output_value = tb.probe.level()  # Get the latest value from the probe
        return output_value == 1  # Return True if tone is detected
    except Exception as e:
        print(f"Error while checking probe output: {e}")
    return False

def main():
    # Initialize the flowgraph
    tb = two_tone_receive()

    # Step 1: Run the transceiver two-tone flowgraph
    run_transceiver_two_tone(tb)

    # Step 2: Start the timer
    start_time = time.perf_counter()

    # Step 3: Continuously check if tones are detected
    while True:
        if check_probe_output(tb):  # Check probe output directly
            elapsed_time = time.perf_counter() - start_time
            print(f"Tones detected! Elapsed time: {elapsed_time:.6f} seconds")
            break
        else:
            time.sleep(0.01)  # Check frequently

    # Step 4: Terminate the flowgraph after detection
    tb.stop()
    tb.wait()
    print("Transceiver process terminated.")

    return elapsed_time

if __name__ == "__main__":
    main()

