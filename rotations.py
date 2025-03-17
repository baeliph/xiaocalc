class Rotation:
    """
    Represents a Xiao rotation. These classes allow the user to define all dynamic buffs
    differently depending on the hit count for each rotation.
    """

    def __str__(self):
        return self.__class__.__name__
    
    def a1_bonus_dmg(self, num_hits):
        """
        Returns the amount of bonus DMG% given by Xiao's A1.
        """
        pass

    def buff_duration_for_benny_ttds_4no(self):
        """
        Returns the number of hits Bennett, TTDS, and 4pc NO buff for.
        """
        pass

    def faruzan_a4_active(self, num_hits):
        """
        Returns true if Faruzann's A4 applies to the given hit.
        """
        pass
    
    def vermillion_stacks(self, num_hits):
        """
        Returns the number of Vermillion stacks to account for.
        """
        pass

    def hunter_stacks(self, num_hits):
        """
        Returns the number of Hunter stacks to account for.
        """
        pass

    def calamity_stacks(self, num_hits):
        """
        Returns the number of Calamity Queller stacks to account for.
        """
        pass

    def engulfing_active(self, num_hits):
        """
        Returns true if Engulfing Lightning's additional ER after Burst is active.
        """
        pass

    def soss_stacks(self, num_hits):
        """
        Returns the number of Staff of the Scarlet Sands stacks to account for.
        """
        pass

    def fanfare(self, num_hits):
        pass

    def fanfare_50(self, num_hits):
        pass   

class EE12HP(Rotation):
    """
    EE Q 12HP.
    """
    
    def a1_bonus_dmg(self, num_hits):
        num_plunge = num_hits - 1
        if num_plunge <= 2:
            return 0.05
        elif num_plunge <= 5:
            return 0.10
        elif num_plunge <= 7:
            return 0.15
        elif num_plunge <= 10:
            return 0.20
        else:
            return 0.25
        
    def buff_duration_for_benny_ttds_4no(self):
        return 8
    
    def faruzan_a4_active(self, num_hits):
        # Faruzan's A4 flat dmg increase is on CD during Xiao's 2nd E.
        return num_hits != 1

    def vermillion_stacks(self, num_hits):
        num_plunge = num_hits - 1
        return min(num_plunge, 4)
    
    def hunter_stacks(self, num_hits):
        # num_plunge = num_hits - 1
        # return min(num_plunge, 3)
        # use flat 3 stacks for furina comps
        return 3
    
    def long_night_oath_stacks(self, num_hits):
        stacks = [0, 0, 2, 3, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4]
        return stacks[num_hits]
    
    def calamity_stacks(self, num_hits):
        if num_hits < 2:
            return 0
        elif num_hits <= 3:
            return num_hits
        elif num_hits <= 4:
            return 5
        else:
            return 6
    
    def engulfing_active(self, num_hits):
        return (num_hits > 1 and num_hits < 11)
    
    def soss_stacks(self, num_hits):
        if num_hits == 1:
            return 1
        elif num_hits > 1 and num_hits < 9:
            return 2
        return 0

    def fanfare(self, num_hits):
        num_plunge = num_hits - 1
        return 36 + 20 * (num_plunge - 1)

    def fanfare_50(self, num_hits):
        if num_hits < 2:
            return 190
        num_plunge = num_hits - 1
        if num_plunge == 1:
            return 230
        elif num_plunge == 2:
            return 245
        elif num_plunge == 3:
            return 280
        else:
            return 300


class EE8N1CJP(Rotation):
    """
    EE Q 8N1CJHP.
    """
    
    def a1_bonus_dmg(self, num_hits):
        if num_hits <= 8:
            return 0.05
        elif num_hits <= 13:
            return 0.10
        elif num_hits <= 20:
            return 0.15
        elif num_hits <= 25:
            return 0.20
        else:
            return 0.25
    
    def buff_duration_for_benny_ttds_4no(self):
        return 17
    
    def faruzan_a4_active(self, num_hits):
        if num_hits == 0 or num_hits == 2 or num_hits == 5:
            # Activates during first E, first N1-1, and first HP
            return True
        elif num_hits >= 6 and num_hits%4 == 0 or num_hits%4 == 1:
            # From 2nd N1CJP onwards, activates on CA and HP
            return True
        return False

    def vermillion_stacks(self, num_hits):
        if num_hits < 5:
            return 0
        elif num_hits == 5:
            return 1
        elif num_hits <= 8:
            return 2
        elif num_hits == 9:
            return 3
        else:
            return 4
        
    def hunter_stacks(self, num_hits):
        if num_hits < 5:
            return 0
        elif num_hits == 5:
            return 1
        elif num_hits <= 8:
            return 2
        else:
            return 3
    
    def calamity_stacks(self, num_hits):
        if num_hits < 2:
            return 0
        elif num_hits <= 4:
            return 2
        elif num_hits == 5:
            return 3
        elif num_hits <= 8:
            return 4
        elif num_hits <= 11:
            return 5
        else:
            return 6

    def engulfing_active(self, num_hits):
        return (num_hits > 1 and num_hits < 26)
    
    def soss_stacks(self, num_hits):
        if num_hits == 1:
            return 1
        elif num_hits > 1 and num_hits < 22:
            return 2
        return 0

class Custom(Rotation):
    pass
