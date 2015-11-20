# -*- coding: utf-8 -*-
import time


class Gpio(object):
    def __init__(self, config):
        self.config = config
        self.intarval = time.time()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.mapping = {
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
        self.initialize()

    def initialize(self):
        for key, value in self.mapping.items():
            GPIO.setup(value["channel"], GPIO.OUT)
            value["pi"].start(0)

    def finalize(self):
        for key, value in self.mapping.items():
            value["pi"].stop()
        GPIO.cleanup()

    def get_region_is_journeys(self, message):
        # Il faut parser le message pour savoir si une recherche d'iti et récupérer le coverage et par la suite la région
        return 'aa'

    def reinitialize(self):
        #self.config.gpio["delay"] est en minute
        if (time.time() - self.intarval) > (self.config.gpio["delay"]*60):
            for key, value in self.mapping.items():
                value["duty"] = 0
                value["pi"].ChangeDutyCycle(value["duty"])
            self.intarval = time.time()

    def manage_lights(self, message):
        self.reinitialize()
        region = self.get_region_is_journeys(message)
        if region:
            if region in self.mapping:
                for key, value in self.mapping.items():
                    if region == key and region in self.config[region]:
                        value["duty"] = value["duty"] + 1
                        duty = (value["duty"]*self.config[region]['max_hits'])/100
                        if duty > 100:
                            duty = 100
                    value["pi"].ChangeDutyCycle(duty)
