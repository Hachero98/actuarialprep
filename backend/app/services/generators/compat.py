"""
Compatibility module replacing scipy functions with numpy/math equivalents.
This allows the generators to run without scipy installed.
"""
import math
import numpy as np


def comb(n, k, exact=True):
    """Binomial coefficient C(n,k)."""
    if k < 0 or k > n:
        return 0
    return math.comb(int(n), int(k))


def perm(n, k, exact=True):
    """Permutations P(n,k)."""
    if k < 0 or k > n:
        return 0
    return math.perm(int(n), int(k))


def ndtr(x):
    """Normal CDF (standard)."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2)))


def ndtri(p):
    """Inverse normal CDF (percent point function). Rational approximation."""
    if p <= 0:
        return -10.0
    if p >= 1:
        return 10.0
    if p == 0.5:
        return 0.0
    # Beasley-Springer-Moro algorithm
    a = [0, -3.969683028665376e+01, 2.209460984245205e+02,
         -2.759285104469687e+02, 1.383577518672690e+02,
         -3.066479806614716e+01, 2.506628277459239e+00]
    b = [0, -5.447609879822406e+01, 1.615858368580409e+02,
         -1.556989798598866e+02, 6.680131188771972e+01,
         -1.328068155288572e+01]
    c = [0, -7.784894002430293e-03, -3.223964580411365e-01,
         -2.400758277161838e+00, -2.549732539343734e+00,
         4.374664141464968e+00, 2.938163982698783e+00]
    d = [0, 7.784695709041462e-03, 3.224671290700398e-01,
         2.445134137142996e+00, 3.754408661907416e+00]
    p_low = 0.02425
    p_high = 1 - p_low
    if p < p_low:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[1]*q+c[2])*q+c[3])*q+c[4])*q+c[5])*q+c[6]) / \
               ((((d[1]*q+d[2])*q+d[3])*q+d[4])*q+1)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        return (((((a[1]*r+a[2])*r+a[3])*r+a[4])*r+a[5])*r+a[6])*q / \
               (((((b[1]*r+b[2])*r+b[3])*r+b[4])*r+b[5])*r+1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[1]*q+c[2])*q+c[3])*q+c[4])*q+c[5])*q+c[6]) / \
                ((((d[1]*q+d[2])*q+d[3])*q+d[4])*q+1)


class NormDist:
    """Minimal normal distribution replacement."""
    def cdf(self, x):
        return ndtr(x)
    def ppf(self, p):
        return ndtri(p)
    def pdf(self, x):
        return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)

class ExponDist:
    def cdf(self, x, scale=1):
        if x < 0: return 0
        return 1 - math.exp(-x / scale)
    def ppf(self, p, scale=1):
        return -scale * math.log(1 - p)

class GammaDist:
    """Minimal gamma distribution — only supports integer shape (Erlang)."""
    def cdf(self, x, a, scale=1):
        # Use incomplete gamma via series for small integer a
        z = x / scale
        if z <= 0: return 0
        s = 0
        term = 1
        for k in range(int(a)):
            if k > 0:
                term *= z / k
            s += term
        return 1 - math.exp(-z) * s

class BinomDist:
    def pmf(self, k, n, p):
        return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
    def cdf(self, k, n, p):
        return sum(self.pmf(i, n, p) for i in range(int(k) + 1))

class PoissonDist:
    def pmf(self, k, mu):
        return math.exp(-mu) * (mu ** k) / math.factorial(int(k))
    def cdf(self, k, mu):
        return sum(self.pmf(i, mu) for i in range(int(k) + 1))


norm = NormDist()
expon = ExponDist()
gamma = GammaDist()
binom = BinomDist()
poisson = PoissonDist()
