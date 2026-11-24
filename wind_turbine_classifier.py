import random


class WindTurbine:
    def __init__(self, cut_in_speed, rated_speed, cut_out_speed, rated_mw):
        self.cut_in_speed = cut_in_speed #minimum wind speed to start generating power
        self.rated_speed = rated_speed #wind speed at which the turbine generates its rated power
        self.cut_out_speed = cut_out_speed #wind speed at which the turbine stops generating power to prevent damage
        self.rated_mw = rated_mw   #maximum power output of the turbine in megawatts

    def evaluate_speed(self, speed):
        if speed < self.cut_in_speed:
            return "Standby", 0.0
        elif speed < self.rated_speed:
            ratio = (speed - self.cut_in_speed) / (self.rated_speed - self.cut_in_speed)
            return "Partial Load", self.rated_mw * ratio
        elif speed < self.cut_out_speed:
            return "Rated Output", self.rated_mw
        else:
            return "Cut-out", 0.0


class WindMonitor:
    def __init__(self, turbine, wind_speeds):
        self.turbine = turbine
        self.wind_speeds = wind_speeds

    def run(self):
        total_wind_speed = 0.0 #running total of wind speeds to calculate average later
        total_energy_mwh = 0.0

        standby_count = 0 #how many counts of each mode the turbine was in during the monitoring period
        partial_count = 0
        rated_count = 0
        cut_out_count = 0

        print("=== Hourly Wind Turbine Operation Status ===")

        hour = 1
        for speed in self.wind_speeds:
            mode, output_mw = self.turbine.evaluate_speed(speed)

            if mode == "Standby":
                standby_count += 1
            elif mode == "Partial Load":
                partial_count += 1
            elif mode == "Rated Output":
                rated_count += 1
            else:
                cut_out_count += 1

            # Print result
            print(
                f"Hour {hour:2d} | Wind Speed: {speed:5.1f} m/s "
                f"| Mode: {mode:<12} | Est. Output: {output_mw:4.2f} MW"
            )

            total_wind_speed += speed
            total_energy_mwh += output_mw #predicted energy output in MWh for that hour
            hour += 1

        # Print summary
        total_hours = len(self.wind_speeds)
        average_wind_speed = total_wind_speed / total_hours

        print("\n=== Operation Summary ===")
        print(f"Total Hours Checked   : {total_hours} hrs")
        print(f"Average Wind Speed    : {average_wind_speed:.2f} m/s")
        print(f"Total Est. Generation : {total_energy_mwh:.2f} MWh")
        print("--- Mode Counts ---")
        print(f"Standby               : {standby_count}")
        print(f"Partial Load          : {partial_count}")
        print(f"Rated Output          : {rated_count}")
        print(f"Cut-out               : {cut_out_count}")


# random 10housrs 0.5 and 26.0 m/s
wind_speeds = []
for i in range(10):
    random_speed = round(random.uniform(0.5, 26.0), 1)
    wind_speeds.append(random_speed)

# Create objects and run
turbine = WindTurbine(
    cut_in_speed=3.0,
    rated_speed=12.0,
    cut_out_speed=25.0,
    rated_mw=5.0,
)
monitor = WindMonitor(turbine=turbine, wind_speeds=wind_speeds)
monitor.run()