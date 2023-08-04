# car_sections = [
#     "Engine Maintenance",
#     "Brakes and Suspension",
#     "Electrical System",
#     "Fluids and Lubrication",
#     "Tires and Wheels",
#     "Body and Interior",
#     "HVAC System"
# ]
# car_dict = {}
# car_dict["Engine Maintenance"] = ["Oil changes", "Filter replacements",
#                                   "Spark plug replacements", "Timing belt inspection", "Air intake cleaning"]
# car_dict["Brakes and Suspension"] = ["Brake pad replacements", "Rotor replacements",
#                                      "Suspension checks", "Wheel bearing inspection", "Shock absorber replacements"]
# car_dict["Electrical System"] = ["Battery health check", "Alternator replacement",
#                                  "Wiring inspection", "Starter motor replacement", "Fuse box inspection"]
# car_dict["Fluids and Lubrication"] = ["Coolant level check", "Transmission fluid replacement",
#                                       "Power steering fluid top-up", "Brake fluid flush", "Windshield washer fluid refill"]
# car_dict["Tires and Wheels"] = ["Tire pressure maintenance", "Tire rotation",
#                                 "Wheel alignment", "Tire tread depth check", "Wheel balancing"]
# car_dict["Body and Interior"] = ["Car washing", "Interior cleaning",
#                                  "Cosmetic repairs", "Seat upholstery cleaning", "Dashboard polishing"]
# car_dict["HVAC System"] = ["Filter replacements", "Refrigerant level check",
#                            "System functionality test", "Heater core inspection", "A/C compressor replacement"]
# for kind in car_dict:
#     models.MainSection(name=kind).save()
#     # pk = models.MainSection.objects.filter(name=kind)
#     # for d in car_dict[kind]:
#     #     models.TechnicalCondition()
# data = models.MainSection.objects.all().values()
