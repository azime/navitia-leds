import time
import csv

delay = 0.2
maxi = 2289
file_name = "regions.csv"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

mapping = {
    "le-de-France": {"pi": GPIO.PWM(16, 100), "channel": 16, "duty": 0},
    "Alsace": {"pi": GPIO.PWM(29, 100), "channel": 29, "duty": 0},
    "Aquitaine": {"pi": GPIO.PWM(31, 100), "channel": 31, "duty": 0},
    "Auvergne": {"pi": GPIO.PWM(12, 100), "channel": 12, "duty": 0},
    "Basse-Normandie": {"pi": GPIO.PWM(11, 100), "channel": 11, "duty": 0},
    "Bourgogne": {"pi": GPIO.PWM(18, 100), "channel": 18, "duty": 0},
    "Bretagne": {"pi": GPIO.PWM(7, 100), "channel": 7, "duty": 0},
    "Centre-Val de Loire": {"pi": GPIO.PWM(22, 100), "channel": 22, "duty": 0},
    "Champagne-Ardenne": {"pi": GPIO.PWM(29, 100), "channel": 29, "duty": 0},
    "Franche-Comte": {"pi": GPIO.PWM(18, 100), "channel": 18, "duty": 0},
    "Haute-Normandie": {"pi": GPIO.PWM(11, 100), "channel": 11, "duty": 0},
    "Languedoc-Roussillon": {"pi": GPIO.PWM(33, 100), "channel": 33, "duty": 0},
    "Limousin": {"pi": GPIO.PWM(31, 100), "channel": 31, "duty": 0},
    "Lorraine": {"pi": GPIO.PWM(29, 100), "channel": 29, "duty": 0},
    "Midi-Pyrenees": {"pi": GPIO.PWM(33, 100), "channel": 33, "duty": 0},
    "Nord-Pas-de-Calais": {"pi": GPIO.PWM(15, 100), "channel": 15, "duty": 0},
    "Picardie": {"pi": GPIO.PWM(15, 100), "channel": 15, "duty": 0},
    "Pays de la Loire": {"pi": GPIO.PWM(13, 100), "channel": 13, "duty": 0},
    "Poitou-Charentes": {"pi": GPIO.PWM(31, 100), "channel": 31, "duty": 0},
    "Provence-Alpes-Cote d'Azur": {"pi": GPIO.PWM(35, 100), "channel": 35, "duty": 0},
    "Rhone-Alpes": {"pi": GPIO.PWM(12, 100), "channel": 12, "duty": 0},
}

for key, value in mapping.items():
    GPIO.setup(value["channel"], GPIO.OUT)


def initialize_gpio():
    for key, value in mapping.items():
        value["pi"].start(0)

initialize_gpio()

try:
    with open(file_name) as filep:
        while True:
            filep.seek(0)
            reader = csv.DictReader(filep, delimiter=",")
            print "start reading..."
            for row in reader:
                print row
                region = row['region']

                if region in mapping:
                    for key, value in mapping.items():
                        if region == key:
                            duty = int(row['count']) * 18
                            if duty > 100:
                                duty = 100
                            value["duty"] = duty
                        else:
                            value["duty"] *= 0.8

                        value["pi"].ChangeDutyCycle(value["duty"])
                time.sleep(delay)

except KeyboardInterrupt:
    for key, value in mapping.items():
        value["pi"].stop()
    GPIO.cleanup()  # clean up GPIO on CTRL+C exit


