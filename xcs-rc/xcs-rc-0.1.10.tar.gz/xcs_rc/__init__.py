# -*- coding: utf-8 -*-
"""
Created on Mon Jul 1 10:13:54 2019
@author: Nugroho Fredivianus
"""

# TODO: multistep
# TODO: feature selection

# initial values
cond_init = []
act_init = 0
pred_init = 50.0
prederr_init = 0.0
fit_init = 10.0


class Agent(object):

    def __init__(self):
        # user-defined scenario
        self.num_actions = 2
        self.maxreward = 100.0
        self.multistep = 0

        # xcs parameters
        self.maxpopsize = 100
        self.alpha = 0.1
        self.beta = 0.15
        self.gamma = 0.5
        self.delta = 0.1
        self.nu = 5.0
        self.epsilon_0 = 0.01
        self.theta_del = 25
        self.theta_sub = 20
        self.xmax = 50  # was teletransportation

        # rc parameters
        self.minexp = 1  # minimum experience to be combined
        self.tcomb = 50  # combining period T_comb
        self.predtol = 20.0  # prediction tolerance, maximum difference allowed to be combined
        self.prederrtol = 10.0  # prediction error tolerance, threshold for hasty combining detection

        self.pop = []  # population
        self.mset = []  # match set
        self.aset = []  # action set
        self.xset = []  # multistep set = collection of rules entering action set from its last update
        self.trials = 0
        self.pop_changed = False

    def build_matchset(self, state):
        self.mset = []
        covered_actions = [False for x in range(self.num_actions)]
        for cl in self.pop:
            if cl.match(state):
                covered_actions[cl.act] = True
                self.mset.append(cl)

        if not all(covered_actions):
            for i in range(len(covered_actions)):
                if not covered_actions[i]:
                    cl = Classifier(cond=floatify(state), act=i)
                    self.mset.append(cl)

    def pick_action_winner(self, exploring=False):
        pa = [0.0 for x in range(self.num_actions)]
        ft = [0.0 for x in range(self.num_actions)]
        exp = [0 for x in range(self.num_actions)]
        inexp = [0 for x in range(self.num_actions)]

        for cl in self.mset:
            pa[cl.act] += cl.pred * cl.fit
            ft[cl.act] += cl.fit
            exp[cl.act] += cl.exp
            inexp[cl.act] += 1 if cl.exp == 0 else 0

        if min(pa) == max(pa):  # if all predictions are equal
            pa = [1.0 for x in range(self.num_actions)]
        else:
            for i in range(len(pa)):
                pa[i] /= ft[i]

        if exploring:
            if max(inexp) > 0:
                pick = inexp.index(max(inexp))
            else:
                pick = choice(pa, 1)[0]
        else:
            if pa.count(max(pa)) > 1:
                pick = exp.index(max(exp))
            else:
                pick = pa.index(max(pa))

        return int(pick)

    def build_actionset(self, winner):
        for cl in self.mset:
            if cl.act == winner:
                self.aset.append(cl)
                if cl.exp == 0:
                    self.pop.append(cl)
                    self.pop_changed = True

        if self.multistep > 0:
            self.xset.append(self.aset)
            if len(self.xset) > self.multistep:
                self.xset.pop(0)

        if self.pop_changed:
            sumnum = 0
            for cl in self.pop:
                sumnum += cl.num
            if sumnum > self.maxpopsize:
                self.del_from_pop(sumnum - self.maxpopsize)

    def apply_reward(self, reward):
        P = reward
        to_del = []

        for cl in self.aset:
            prev = cl.prederr
            cl.exp += 1
            cl.update_prederr(P, self.beta)
            cl.update_pred(P, self.beta)

            if cl.prederr > self.prederrtol > prev and cl.prederr >= prev and cl.exp > 2 * self.minexp:
                to_del.append(cl)  ### directly removing the classifier with high prederr
                # another option: reduce its numerosity first, suitable for a more dynamic environment
                # cl.num = 0 if removal_atonce else cl.num - 1
                # if cl.num == 0:
                #     to_del.append(cl)
            else:
                if cl.exp == self.minexp:
                    self.pop_changed = True

        if len(to_del) > 0:
            self.pop = [x for x in self.pop if x not in to_del]
            self.aset = [x for x in self.aset if x not in to_del]
            if self.multistep > 0:
                for xsubset in self.xset:
                    xsubset = [x for x in xsubset if x not in to_del]

        self.update_fitset()

        self.trials += 1
        if self.tcomb > 0 and self.trials % self.tcomb == 0 and self.pop_changed:
            self.sort_pop()
            self.combine_pop()
            self.pop_changed = False

        self.aset = []

    def apply_xreward(self, reward):
        P = reward + self.gamma * self.maxreward  # gamma for multistep
        for xsubset in self.xset:
            for cl in xsubset:
                cl.exp += 1
                cl.update_prederr(P)
                cl.update_pred(P)

        self.pop_changed = True
        self.xset = [[]]

    def combine_pop(self):
        import math

        for loop in range(2):
            for act in range(self.num_actions):
                cset = [cl for cl in self.pop if cl.act == act]
                cl_del = []
                for i in range(len(cset)):
                    for j in range(i + 1, len(cset)):
                        if i != j and cset[i].exp >= self.minexp and cset[i] not in cl_del and cset[j] not in cl_del and \
                                cset[j].exp >= self.minexp and abs(cset[i].pred - cset[j].pred) <= self.predtol:
                            clstar = Classifier(cond=combine_cond(cset[i].cond, cset[j].cond), act=act)
                            clstar.pred = (cset[i].pred * cset[i].num + cset[j].pred * cset[j].num) / (
                                    cset[i].num + cset[j].num)

                            disproval_found = False

                            for k in range(len(cset)):
                                if (k != i and k != j and cset[k] not in cl_del and cset[k].exp > 0 and cset[k].overlap(
                                        clstar) and not within_range(clstar.pred, cset[k].pred, self.predtol)):
                                    disproval_found = True
                                    break

                            if not disproval_found:
                                cl_pred = 0.0
                                cl_num = 0
                                cl_exp = 0

                                for n in range(len(cset)):
                                    itspred = cset[n].pred
                                    itsexp = cset[n].exp
                                    inrange = (
                                                itspred + self.predtol >= clstar.pred and itspred <= clstar.pred + self.predtol)

                                    if cset[n].subsumable_to(clstar) and (inrange or itsexp == 0):
                                        cl_del.append(cset[n])

                                        if itsexp > 0:
                                            cl_exp += itsexp
                                            cl_num += cset[n].num
                                            cl_pred += cset[n].pred * cset[n].num

                                cl_pred /= cl_num

                                exp_lim = 1 / self.beta
                                cl_prederr = abs(cl_pred - pred_init) / cl_exp if cl_exp <= math.floor(exp_lim) else (
                                                                                                                             abs(
                                                                                                                                 cl_pred - pred_init) / exp_lim) * math.pow(
                                    1 - self.beta, cl_exp - math.floor(exp_lim))
                                cl_fit = (fit_init - 1) * math.pow(1 - self.beta, cl_exp) + 1

                                clstar.num += cl_num - 1
                                clstar.exp = cl_exp
                                clstar.pred = cl_pred
                                clstar.fit = cl_fit
                                clstar.prederr = cl_prederr

                                self.pop.append(clstar)
                                cset.append(clstar)

                self.pop = [x for x in self.pop if x not in cl_del]

        self.pop = [cl for cl in self.pop if cl.exp > 0]  ### optionally remove inexperienced rules

    def next_action(self, state, explore):
        self.build_matchset(state)
        action = self.pick_action_winner(explore)
        self.build_actionset(action)
        return action

    def del_from_pop(self, deletion):
        inexps = [cl for cl in self.pop if cl.exp == 0]
        if len(inexps) > 0:
            self.pop = [cl for cl in self.pop if cl not in inexps]

        if deletion > len(inexps):
            store = []

            dummy = self.pop.copy()
            for cl in self.pop:
                if cl in self.mset:
                    store.append(cl)
                    dummy.remove(cl)

            sumfit = 0.0
            sumnum = 0.0
            for cl in dummy:
                sumfit += cl.fit
                sumnum += cl.num
            meanfit = sumfit / sumnum

            points = []
            for cl in dummy:
                points.append(cl.get_delprop(meanfit, self.delta, self.theta_del))

            dels = [dummy[x] for x in choice(points, deletion)]

            for cl_del in dels:
                cl_del.num -= 1
                if cl_del.num <= 0:
                    dummy.remove(cl_del)

            self.pop = dummy + store

    def update_fitset(self):
        sumacc = 0.0
        acc = [0.0 for x in range(len(self.aset))]

        for i in range(len(self.aset)):
            acc[i] = self.aset[i].get_accuracy(self.alpha, self.epsilon_0, self.nu)
            sumacc += acc[i] * self.aset[i].num

        for i in range(len(self.aset)):
            self.aset[i].update_fitness(sumacc, acc[i], self.beta)

    def sort_pop(self, opt=0):  ### 0 exp, 1 pred, 2 act, 3 num
        if opt == 1 or opt == "pred":
            self.pop.sort(key=lambda cl: cl.pred, reverse=True)
        elif opt == 2 or opt == "act":
            self.pop.sort(key=lambda cl: cl.act, reverse=False)
        elif opt == 3 or opt == "num":
            self.pop.sort(key=lambda cl: cl.num, reverse=True)
        else:
            self.pop.sort(key=lambda cl: cl.exp, reverse=True)

    def insert_to_pop(self, data):
        if isinstance(data, str):
            import os.path
            if os.path.isfile(data):
                with open(data) as f:
                    cls = f.readlines()
            else:
                print("File " + data + " does not exist. Init failed.")
                return False
        elif isinstance(data, list):
            cls = data
        else:
            return False

        for cl in cls:
            if cl[0].isdigit():
                z = cl.count(";")
                val = cl.split(";")
                val_cond = ""
                for i in range(1, z - 6):
                    val_cond += val[i] + ","
                self.pop.append(
                    Classifier(cond=floatify(val_cond[:-1]), act=int(val[z - 6]), pred=float(val[z - 5]),
                               fit=float(val[z - 4]), prederr=float(val[z - 3]), num=int(val[z - 2]),
                               exp=int(val[z - 1]), actsetsize=int(val[z])))
        print("Pop initialized: {} classifiers.".format(len(self.pop)))

    def print_pop(self, title=""):
        print_set(self.pop, title, True)

    def save_popfile(self, fname, title="", save_mode='w', feedback=False):
        if save_mode != 'a':
            save_mode = 'w'
        try:
            with open(fname, save_mode) as f:
                if save_mode == 'a':
                    f.write(".\n")  # vertical separator
                if title != "":
                    f.write(title + "\n")
                f.write(get_header(self.pop[0]) + "\n")
                write_classifiers(self.pop, f)
            if feedback:
                print("Population is stored to {}: {} classifiers.".format(fname, len(self.pop)))
        except:
            print("Failed to save population.")

    def train(self, X_train, y_train, show_progress=True):
        X_train = get_list(X_train)
        y_train = get_list(y_train)
        self.num_actions = len(set(y_train))

        for i in range(len(X_train)):
            answer = self.next_action(X_train[i], True)  # always exploring
            reward = int(answer == y_train[i]) * self.maxreward
            self.apply_reward(reward)

            # simple progress visualization
            if show_progress:
                print('.', end='')
                if i % 100 == 99:
                    print()

        self.sort_pop()
        return self.pop

    def test(self, X_test, y_test, show_progress=True):
        X_test = get_list(X_test)
        y_test = get_list(y_test)
        cm = [[0 for x in range(self.num_actions)] for y in range(self.num_actions)]

        for i in range(len(y_test)):
            answer = self.next_action(X_test[i], False)  # always exploiting
            cm[y_test[i]][answer] += 1

            # simple progress visualization
            if show_progress:
                print('.', end='')
                if i % 100 == 99:
                    print()

        return cm


# Classifier class

class Classifier(object):
    global cond_init, act_init, pred_init, fit_init, prederr_init

    def __init__(self, cond=cond_init, act=act_init, pred=pred_init,
                 fit=fit_init, prederr=prederr_init, num=1, exp=0, actsetsize=1):

        number = (int, float, complex)
        new_cond = []

        if cond != cond_init:
            if isinstance(cond, str):
                if not is_binarystr(cond):
                    return
                for c in cond:
                    el = [0.000, 0.000] if c == '0' else [1.000, 1.000]
                    new_cond.append(el)

            elif isinstance(cond, list):
                for c in cond:
                    el = []
                    if isinstance(c, list):
                        if len(c) != 2:
                            print("Cl cond: number of elements error.")
                            return

                        for c2 in c:
                            if not isinstance(c2, number):
                                print("Cl cond: value error.")
                                return

                        el = [min(c), max(c)]

                    elif isinstance(c, number):
                        el = [c, c]

                    new_cond.append(el)

        else:
            new_cond = cond

        if not isinstance(act, int):
            print("Cl act: not an integer.")
            return

        self.cond = new_cond
        self.act = act

        self.pred = pred
        self.prederr = prederr
        self.fit = fit
        self.num = num
        self.exp = exp
        self.actsetsize = actsetsize

    def match(self, cl):
        if isinstance(cl, Classifier):
            if cl.act != self.act:
                return False
            state = cl.cond
        else:
            state = cl

        if len(state) != len(self.cond):
            return False
        if isinstance(state, str):
            if not is_binarystr(state):
                return False
            state = binarytolist(state)

        for sc, st in zip(self.cond, state):
            if st < sc[0] or st > sc[1]:
                return False

        return True

    def copy(self):
        cl = Classifier(cond=self.cond, act=self.act, pred=self.pred, prederr=self.prederr, fit=self.fit, num=self.num,
                        exp=self.exp, actsetsize=self.actsetsize)
        return cl

    def subsumable_to(self, cl):
        if not isinstance(cl, Classifier):
            return False
        if cl.act != self.act:
            return False
        if len(cl.cond) != len(self.cond):
            return False

        for sc, cc in zip(self.cond, cl.cond):
            if sc[0] < cc[0] or sc[1] > cc[1]:
                return False

        return True

    def can_subsume(self, cl):
        if not isinstance(cl, Classifier):
            return False
        if cl.act != self.act:
            return False
        if len(cl.cond) != len(self.cond):
            return False

        for sc, cc in zip(self.cond, cl.cond):
            if sc[0] > cc[0] or sc[1] < cc[1]:
                return False

        return True

    def resemblance(self, cl):
        if not isinstance(cl, Classifier):
            return 0
        if len(cl.cond) != len(self.cond):
            return 0

        res = 0
        for sc, cc in zip(self.cond, cl.cond):
            if cc[1] >= sc[0] and cc[0] <= sc[1]:
                res += 1

        return res

    def overlap(self, cl):
        if not isinstance(cl, Classifier):
            return False
        if len(self.cond) != len(cl.cond):
            return False

        for sc, cc in zip(self.cond, cl.cond):
            if cc[0] > sc[1] or sc[0] > cc[1]:
                return False
        return True

    def get_delprop(self, meanfit, delta, theta_del):
        if self.fit / self.num >= delta * meanfit or self.exp < theta_del:
            return self.actsetsize * self.num
        return self.actsetsize * self.num * meanfit / (self.fit / self.num)

    def update_pred(self, P, beta):
        if self.exp < 1. / beta:
            self.pred = (self.pred * (self.exp - 1.0) + P) / self.exp
        else:
            self.pred += beta * (P - self.pred)

        return self.pred * self.num

    def update_prederr(self, P, beta):
        if self.exp < 1.0 / beta:
            self.prederr = (self.prederr * (self.exp - 1.0) + abs(P - self.pred)) / self.exp
        else:
            self.prederr += beta * (abs(P - self.pred) - self.prederr)

        return self.prederr * self.num

    def get_accuracy(self, alpha, epsilon_0, nu):
        import math
        if self.prederr <= epsilon_0:
            accuracy = 1.0
        else:
            accuracy = alpha * math.pow(self.prederr / epsilon_0, -nu)
        return accuracy

    def update_fitness(self, accsum, accuracy, beta):
        if accsum != 0:
            self.fit += beta * ((accuracy * self.num) / accsum - self.fit)
        return self.fit

    def update_actsetsize(self, numsum, beta):
        if self.exp < 1. / beta:
            self.actsetsize = (self.actsetsize * (self.exp - 1) + numsum) / self.exp
        else:
            self.actsetsize += beta * (numsum - self.actsetsize)
        return self.actsetsize * self.num

    def printable(self):
        return "{0};{1};{2:.3f};{3:.3f};{4:.3f};{5};{6};{7}".format(self.printable_cond(), self.act, self.pred,
                                                                    self.fit, self.prederr, self.num, self.exp,
                                                                    self.actsetsize)

    def print(self, title=False):
        if title:
            print("Cond:Act->Pred | Fit, PredErr, Num, Exp, ActSetSize")
        print(self.printable())

    def has_binarycond(self):
        for sc in self.cond:
            if (sc[0] != 0.0 and sc[0] != 1.0) or (sc[1] != 0.0 and sc[1] != 1.0):
                return False
        return True

    def printable_cond(self):
        str_cond = ""
        if self.has_binarycond():
            str_cond = '"'
            for sc in self.cond:
                str_cond += "#" if sc[0] != sc[1] else "0" if sc[0] == 0.0 else "1"
            str_cond += '"'
        else:
            for c in self.cond:
                if isinstance(c, list):
                    if isinstance(c[0], int):
                        c0 = "[{}".format(c[0])
                        c1 = "[{}".format(c[1])
                    elif (c[0]).is_integer():
                        c0 = "[{}".format(int(c[0]))
                        c1 = "[{}".format(int(c[1]))
                    else:
                        c0 = "[{0:.3f}".format(c[0])
                        c1 = "[{0:.3f}".format(c[1])
                    str_cond += c0
                    if c[0] != c[1]:
                        str_cond += c1
                    str_cond += "];"
                else:
                    str_cond += "{0:.3f}".format(c)
            str_cond = str_cond[:-1]

        return str_cond


def is_binarystr(str_cond):
    for s in str_cond:
        if s not in "10":
            print("Cl cond: binary error.")
            return False
    return True


def binarytolist(val):
    cond = []
    for v in val:
        c = 0.000 if v == '0' else 1.000
        cond.append(c)
    return cond


def floatify(state):
    cond = []
    if isinstance(state, str):
        if state[0] == '[':
            states = state.split('],[')
            for s in states:
                s = s.replace('[', '').replace(']', '')
                a = [0, 0]
                if s.count(',') == 1:
                    a = s.split(',')
                else:
                    a[0] = s
                    a[1] = s
                cond.append([float(a[0]), float(a[1])])
        else:
            for s in state:
                if s not in "10":
                    return False
                if s == "0":
                    cond.append([0.00, 0.00])
                else:
                    cond.append([1.00, 1.00])

    elif isinstance(state, list):
        for s in state:
            cond.append([s, s])

    return cond


def write_classifiers(cls, f):
    i = 0
    for cl in cls:
        i += 1
        f.write("{};{}\n".format(i, cl.printable()))


def get_header(cl):
    head = "id;cond;"
    if not cl.has_binarycond():
        for i in range(len(cl.cond) - 1):
            head += ";"
    head += "act;pred;fit;prederr;num;exp;actsetsize"

    return head


def print_set(myset, title="", header=True):
    if title != "":
        print(".\n" + title)

    if len(myset) > 0:
        if header:
            print(get_header(myset[0]))
        i = 0
        for cl in myset:
            i += 1
            print("{};{}".format(i, cl.printable()))
    else:
        if title != "":
            print("[empty]")


def within_range(val1, val2, tol):
    return val2 + tol >= val1 and val2 <= val1 + tol


def combine_cond(cond1, cond2):
    dummy = [[-1.0, -1.0] for x in range(len(cond1))]
    for i in range(len(cond1)):
        dummy[i] = [min(cond1[i][0], cond2[i][0]), max(cond1[i][1], cond2[i][1])]
    return dummy


def choice(arr, times):
    import random

    if times > len(arr):
        return []
    elif times == len(arr):
        picks = list(range(times))
        random.shuffle(picks)
        return picks

    sums = 0.0
    sum_array = []
    for a in arr:
        sums += a
        sum_array.append(sums)

    picks = [-1]
    for i in range(times):
        chosen = -1

        while chosen in picks:
            val = random.random() * sum(arr)
            chosen = next(i for i, v in enumerate(sum_array) if v > val)
        picks.append(chosen)

    return picks[1:]


def get_list(vals):
    if isinstance(vals, list):
        return vals

    import pandas as pd
    if isinstance(vals, (pd.Series, pd.DataFrame)):
        return vals.values.tolist()

    import numpy as np
    if isinstance(vals, np.ndarray):
        return vals.tolist()

    return None
