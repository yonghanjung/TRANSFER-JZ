import numpy as np
import copy
import itertools
import pandas as pd
from scipy.special import lambertw

class DUCB(object):
    def __init__(self, bound_list, policy_list, Z_obs,  Y_pl_list, X_pl_list, K, T):
        self.bdd_list = bound_list
        self.policy_list = policy_list
        self.policy_idx_list = list(range(len(policy_list)))
        self.Z = Z_obs
        self.Y_list = Y_pl_list
        self.X_list = X_pl_list
        self.K = K
        self.T = T

        self.LB_exp = []
        self.UB_exp = []
        for exp_bdd in bound_list:
            self.LB_exp.append(exp_bdd[0])
            self.UB_exp.append(exp_bdd[1])
        self.l_max = max(self.LB_exp)

        self.mu_list = []
        for idx in range(len(self.Y_list)):
            self.mu_list.append(np.mean(self.Y_list[idx]))
        self.opt_exp = self.mu_list.index(max(self.mu_list))
        self.mu_opt = max(self.mu_list)

    def Exp_Cut(self):
        aftercut_LB_exp = []
        aftercut_UB_exp = []
        aftercut_mu_list = []
        aftercut_policy_idx_list = []

        for sto in self.policy_idx_list:
            lb_e = self.LB_exp[sto]
            ub_e = self.UB_exp[sto]
            if ub_e < self.l_max: # CUT
                continue
            else:
                aftercut_policy_idx_list.append(sto)
                aftercut_LB_exp.append(self.LB_exp[sto])
                aftercut_UB_exp.append(self.UB_exp[sto])
                mu_sto = self.mu_list[sto]
                aftercut_mu_list.append(mu_sto)

        return aftercut_policy_idx_list

    def Compute_divergence_two(self, poly_k, poly_j, Z_obs, Xk):
        pi_k_probs = poly_k.predict_proba(Z_obs)
        pi_j_probs = poly_j.predict_proba(Z_obs)

        sum_elem = 0
        N = len(Z_obs)
        for idx in range(N):
            pi_k_idx = pi_k_probs[idx][Xk[idx]]
            pi_j_idx = pi_j_probs[idx][Xk[idx]]
            sum_elem += np.exp(pi_k_idx / (pi_j_idx + 1e-8)) - 1

        return (sum_elem / N) - 1

    def Compute_Mkj(self, poly_k, poly_j, Z_obs, Xk):
        div_kj = self.Compute_divergence_two(poly_k, poly_j, Z_obs, Xk)
        return np.log(div_kj + 1) + 1

    def Mkj_Matrix(self, policy_list, X_pl_list, Z_obs):
        N_poly = len(policy_list)
        poly_idx_iter = list(itertools.product(list(range(N_poly)), list(range(N_poly))))
        M_mat = np.zeros((N_poly, N_poly))
        for k, j in poly_idx_iter:
            # if k != j:
            poly_k = policy_list[k]
            poly_j = policy_list[j]
            Xk = X_pl_list[k]
            M_mat[k, j] = self.Compute_Mkj(poly_k, poly_j, Z_obs, Xk)
        return M_mat

    def Poly_ratio_kj(self,poly_k, poly_j, zs, xj_s):
        return poly_k.predict_proba(zs)[xj_s] / poly_j.predict_proba(zs)[xj_s]

    def Clipped_est(self, k, Ns, M, policy_idx_list, policy_list, Tau_s, Y_pl_list, Z_obs, X_pl_list, t):
        eps_t = 2 / t
        poly_k = policy_list[k]
        Zk_t = 0
        for j in policy_idx_list:
            Zk_t += Ns[j] / M[k, j]

        mu_k = 0
        for j in policy_idx_list:
            poly_j = policy_list[j]
            Xj = X_pl_list[j]
            for s in Tau_s[j]:
                if self.Poly_ratio_kj(poly_k, poly_j, Z_obs.ix[s], Xj[s]) < 2 * np.log(2 / eps_t) * M[k, j]:
                    mu_k += (1 / M[k, j]) * (Y_pl_list[j][s]) * self.Poly_ratio_kj(poly_k, poly_j, Z_obs.ix[s], Xj[s])
                else:
                    continue
        mu_k = mu_k / Zk_t
        return mu_k

    def Upper_bonus(self, k, Ns, M, policy_idx_list, t):
        Zk_t = 0
        c1 = 16
        for j in policy_idx_list:
            Zk_t += Ns[j] / M[k, j]
        C = (np.sqrt(c1 * t * np.log(t))) / (Zk_t)
        Bt = np.real(C * lambertw(2 / (C + 1e-8)))
        Sk = 1.5 * Bt
        return Sk

    def policy_pull(self, poly, zt):


    def DUCB(self):
        Ns = dict()
        Tau_s = dict()
        sum_reward = 0
        cum_regret = 0
        Reward_arm = dict()

        prob_opt_list = []
        cum_regret_list = []
        Sto_pick = []

        for s in self.policy_idx_list:
            Ns[s] = 0
            Tau_s[s] = []
            Reward_arm[s] = []
        # Initial pulling
        for t in range(self.K * len(self.policy_idx_list)):
            # Policy pick!
            st = np.mod(t, len(self.policy_idx_list))
            zt = self.Z.ix[t]

            # Policy choosing arm
            at = self.X_list[st].ix[t]
            poly_st

            rt = self.Pull_Receive(at, Na_T)

            Tau_s[st].append(st)
            Ns[st] += 1
            Sto_pick.append(st)


            Reward_arm[at].append(rt)
            sum_reward += rt

            prob_opt = Na_T[self.opt_arm] / (t + 1)
            cum_regret += self.u_opt - u_list[at]

            prob_opt_list.append(prob_opt)
            cum_regret_list.append(cum_regret)







    # def pairwise(self,iterable):
    #     "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    #     a = iter(iterable)
    #     return zip(a, a)
    #
    # def MedianofMeans(self, A, ngroups=55):
    #     '''Calculates median of means given an Array A, ngroups is the number of groups '''
    #     if ngroups > len(A):
    #         ngroups = len(A)
    #     Aperm = np.random.permutation(A)
    #     try:
    #         lists = np.split(Aperm, ngroups)
    #     except:
    #         x = len(A) / ngroups
    #         ng = len(A) / (x + 1)
    #         Atrunc = Aperm[0:ng * x]
    #         lists = np.split(Atrunc, ng) + [Aperm[ng * x::]]
    #     plist = pd.Series(lists)
    #     mlist = plist.apply(np.mean)
    #     return np.median(mlist)
    #
    # def pairmodel_divergence(self, Z, M1, M2, option=1):
    #     '''Function to calculate divergence between two experts
    #     1. When Xtrain is a data-set of features/contexts and M1,M2 are models (eg. xgboost) then we get predict_proba predictions on Xtrain with M1,
    #     M2 and then calculate divergence using the probability values.
    #     2. When Xtrain is none and the probability values themselves are supplied as M1, M2 then the divergence is calculated directly
    #     '''
    #     if Z is None:
    #         P1 = M1
    #         P2 = M2
    #     else:
    #         P1 = M1.predict_proba(Z)
    #         P2 = M2.predict_proba(Z)
    #
    #     if option == 1:
    #         X = P1 / P2
    #         fx = X * np.exp(X - 1) - 1
    #         Efx = P2 * fx
    #         Efx_sum = np.sum(Efx, axis=1)
    #         l = np.where(Efx_sum > 1e100)
    #         inan = np.where(np.isnan(Efx_sum) == True)
    #         Efx_sum[inan] = 1e100
    #         Efx_sum[l] = 1e100
    #         return self.MedianofMeans(Efx_sum)
    #     if option == 2:
    #         X = P1 / P2
    #         fx = X ** 2 - 1
    #         Efx = P2 * fx
    #         Efx_sum = np.sum(Efx, axis=1)
    #         inan = np.where(np.isnan(Efx_sum) == True)
    #         Efx_sum[inan] = 1e10
    #         l = np.where(Efx_sum > 1e10)
    #         Efx_sum[l] = 1e10
    #         return self.MedianofMeans(Efx_sum)



    def Pull_Receive(self, at, Na_T):
        return self.Y_list[at][Na_T[at]]






    def UCB(self, arm_list,u_list, K):
        # LB_arm = self.LB_arm
        # UB_arm = self.UB_arm
        # arm_list = self.arm_list
        # u_list = self.u_list

        # arm_list, LB_arm, UB_arm, u_list = self.Arm_Cut()

        if len(arm_list) == 1:
            print("All cut")
            return arm_list
        else:
            Arm = []
            Na_T = dict()
            sum_reward = 0
            cum_regret = 0
            Reward_arm = dict()

            prob_opt_list = []
            cum_regret_list = []

            # Initial variable setting
            for t in range(len(arm_list)):
                # Before pulling
                at = t
                Na_T[at] = 0
                Reward_arm[at] = []

            # Initial pulling
            for t in range(K*len(arm_list)):
                # Pulling!
                at = np.mod(t, len(arm_list))
                Arm.append(at)
                rt = self.Pull_Receive(at, Na_T)
                Reward_arm[at].append(rt)
                sum_reward += rt
                Na_T[at] += 1
                prob_opt = Na_T[self.opt_arm] / (t + 1)
                cum_regret += self.u_opt - u_list[at]

                prob_opt_list.append(prob_opt)
                cum_regret_list.append(cum_regret)

            # Run!
            UCB_list = []
            X_hat_list = []
            for t in range(K*len(arm_list), self.T):
                UB_list = []
                X_hat_arm = []
                for a in arm_list:
                    # standard UCB
                    x_hat = np.mean(Reward_arm[a])
                    X_hat_arm.append(x_hat)
                    upper_a = np.sqrt( (3 * np.log(t)) / (2 * Na_T[a]))
                    UB_a = x_hat + upper_a
                    UB_list.append(UB_a)
                UCB_list.append(UB_list)
                X_hat_list.append(X_hat_arm)

                at = UB_list.index(max(UB_list))
                Arm.append(at)
                rt = self.Pull_Receive(at, Na_T)

                Reward_arm[at].append(rt)
                sum_reward += rt

                Na_T[at] += 1
                prob_opt = Na_T[self.opt_arm] / (t + 1)
                cum_regret += self.u_opt - u_list[at]

                prob_opt_list.append(prob_opt)
                cum_regret_list.append(cum_regret)
            return prob_opt_list, cum_regret_list, UCB_list, Arm, X_hat_list, Na_T

    def B_UCB(self, K):
        arm_list, LB_arm, UB_arm, u_list = self.Arm_Cut()

        if len(arm_list) == 1:
            print("All cut")
            return arm_list
        else:
            if u_list[0] > u_list[1]:
                opt_arm = 0
                u_opt = u_list[0]
            else:
                opt_arm = 1
                u_opt = u_list[1]

            Arm = []
            Na_T = dict()
            sum_reward = 0
            cum_regret = 0
            Reward_arm = dict()

            prob_opt_list = []
            cum_regret_list = []

            # Initial variable setting
            for t in range(len(arm_list)):
                # Before pulling
                at = t
                Na_T[at] = 0
                Reward_arm[at] = []

            # Initial pulling
            for t in range(K * len(arm_list)):
                # Pulling!
                at = np.mod(t, len(arm_list))
                Arm.append(at)
                rt = self.Pull_Receive(at, Na_T)
                Reward_arm[at].append(rt)
                sum_reward += rt
                Na_T[at] += 1
                prob_opt = Na_T[opt_arm] / (t + 1)
                cum_regret += u_opt - u_list[at]

                prob_opt_list.append(prob_opt)
                cum_regret_list.append(cum_regret)

            # Run!
            UCB_list = []
            UCB_hat_list = []
            X_hat_list = []
            what_choose = []
            for t in range(K * len(arm_list), self.T):
                X_hat_arm = []
                UB_list = []
                UCB_hat = []
                for a in arm_list:
                    # standard UCB
                    x_hat = np.mean(Reward_arm[a])
                    X_hat_arm.append(x_hat)
                    upper_a = np.sqrt((3 * np.log(t)) / (2 * Na_T[a]))
                    UCB_a = x_hat + upper_a
                    UCB_hat.append(UCB_a)
                    UB_a = min(UCB_a, UB_arm[a])
                    UB_list.append(UB_a)
                UCB_list.append(UB_list)
                UCB_hat_list.append(UCB_hat)
                X_hat_list.append(X_hat_arm)

                at = UB_list.index(max(UB_list))
                Arm.append(at)
                rt = self.Pull_Receive(at, Na_T)

                Reward_arm[at].append(rt)
                sum_reward += rt

                Na_T[at] += 1
                prob_opt = Na_T[opt_arm] / (t + 1)
                cum_regret += u_opt - u_list[at]

                prob_opt_list.append(prob_opt)
                cum_regret_list.append(cum_regret)
            return prob_opt_list, cum_regret_list, UCB_list, UCB_hat_list, Arm, X_hat_list, Na_T

    def Bandit_Run(self):
        prob_opt, cum_regret, UCB_list, Arm, X_hat_list,  Na_T = self.UCB(self.arm_list,self.u_list,self.K)
        prob_opt_B, cum_regret_B, UCB_list_B, UCB_hat_list_B, Arm_B,X_hat_list_B, Na_T_B = self.B_UCB(self.K)
        return [[prob_opt, cum_regret, UCB_list, Arm,X_hat_list, Na_T],[prob_opt_B, cum_regret_B, UCB_list_B, UCB_hat_list_B, Arm_B, X_hat_list_B, Na_T_B]]

