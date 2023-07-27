import time

# Death timer class for amount of life lost based on PM2.5 levels in the air
# Based on the following underlying assumptions:
# - Results are a general approximation of the amount of life lost based on the average life expectancy of a person in the UK
# - Results have all the underlying assumptions of the COMEAP report: https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/304641/COMEAP_mortality_effects_of_long_term_exposure.pdf
# - Scaling is linear, i.e. 1ug/m3 in the air = n miliseconds of life lost per second

# 2019 - (Statistics taken pre covid)
# Source: https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/bulletins/nationallifetablesunitedkingdom/2017to2019
EXPECTED_LIFESPAN_MALE = 79.4
EXPECTED_LIFESPAN_FEMALE = 83.1
EXPECTED_LIFESPAN_AVG = (EXPECTED_LIFESPAN_MALE + EXPECTED_LIFESPAN_FEMALE) / 2

# Pulled from: https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/304641/COMEAP_mortality_effects_of_long_term_exposure.pdf
DAYS_SAVED_PER_UG_M3_MALE = 21 # See COMEAP report Table 4.3 (UK average)
DAYS_SAVED_PER_UG_M3_FEMALE = 20 # See COMEAP report Table 4.3 (UK average)
DAYS_SAVED_PER_UG_M3_AVG = (DAYS_SAVED_PER_UG_M3_MALE + DAYS_SAVED_PER_UG_M3_FEMALE) / 2



class DeathTimer():
    def __init__(self):
        self.start_time = None
        self.cumulative_life_lost_ms = 0
        self.ug_m3 = 0
    
    def start(self):
        self.start_time = time.ticks_ms()
        self.last_update_time = self.start_time
    
    def tick(self):
        if self.start_time is None:
            raise Exception("Cannot tick before starting the timer")
        now = time.ticks_ms()
        delta = now - self.last_update_time
        self.last_update_time = now
        self.cumulative_life_lost_ms += self._caclulate_lost_life_ms(delta)
    
    def set_ug_m3(self, ug_m3):
        self.ug_m3 = ug_m3
    
    def get_cumulative_life_lost_ms(self):
        return self.cumulative_life_lost_ms
    
    # Calculates the amount of life lost im MS based on a given delta in MS
    def _caclulate_lost_life_ms(self, delta):
        expected_ls_days = EXPECTED_LIFESPAN_AVG * 365.2425
        expected_ls_lost_days = DAYS_SAVED_PER_UG_M3_AVG * self.ug_m3
        ratio_of_life_lost = expected_ls_lost_days / expected_ls_days
        return delta * ratio_of_life_lost