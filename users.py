import pandas as pd
import numpy as np
np.random.seed(5)


class Users:
    """ User group characteristics """

    def __init__(self, city, aggregate=True):
        assert isinstance(city, str)
        self.city = city
        if aggregate:
            self.raw_od = pd.read_csv("Locations/" + city + "/od.csv")
        else:
            self.raw_od = pd.read_csv("Locations/" + city + "/od_groups.csv")
        self.num_users = None
        self.vot_mean_array = None
        self.data = self._generate_users()
        self.native_OD_demand = [self.data[i]['vol'] for i in range(len(self.data))]

    def _generate_users(self):

        df = self.raw_od
        self.num_users = df.shape[0]
        self.vot_mean_array = df['vot'].to_numpy() # CHECK!

        df['vot'] = self.vot_realization()

        df.rename(columns={"origin": "orig", "destination": "dest", "volume": "vol", "vot": "vot", "income": "income"}, inplace=True)
        data = df.to_dict('index')
        return data

    def vot_list(self):
        vot = [self.data[i]['vot'] for i in range(len(self.data))]
        return vot

    def vot_array(self):
        vot = [self.data[i]['vot'] for i in range(len(self.data))]
        return np.array(vot)

    def income_list(self):
        income = [self.data[i]['income'] for i in range(len(self.data))]
        return income

    def income_array(self):
        income = [self.data[i]['income'] for i in range(len(self.data))]
        return np.array(income)

    def user_flow_list(self):
        user_flow = [self.data[i]['vol'] for i in range(len(self.data))]
        return user_flow

    def vot_realization(self, fixed_vot=False):
        if fixed_vot is True:
            vot_array = np.ones(self.num_users)
        elif type(fixed_vot) is float:
            vot_array = fixed_vot * np.ones(self.num_users)
        else:
            vot_array = self.vot_mean_array
        return vot_array

    def new_instance(self, fixed_vot=False):
        new_vot = self.vot_realization(fixed_vot=fixed_vot)
        for u in self.data.keys():
            self.data[u]['vot'] = new_vot[u]
        return None

    def od_realization(self):
        new_vol = np.zeros(len(self.num_users))
        for od_index in range(self.num_users):
            for user_index in self.native_OD_demand[od_index]:
                if np.random.rand() < 0.8:
                    new_vol[od_index] += 1
                else:
                    new_route = np.random.randint(0, self.num_users-1)
                    new_vol[new_route] += 1
        return new_vol

    def new_iid_od_instance(self):
        self.new_instance()
        new_vol = self.od_realization()
        for u in self.data.keys():
            self.data[u]['vol'] = new_vol[u]
        return None

    def population_vot_mean(self):
        weighted_sum = 0
        total_sum = 0
        for u in self.data.keys():
            weighted_sum += self.data[u]['vol'] * self.vot_mean_array[u]
            total_sum += self.data[u]['vol']
        return weighted_sum / total_sum
