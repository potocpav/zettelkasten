---
date: 2021-07-11T09:55
tags:
  - astronomy
  - experiment
---

# Measuring Moon Distance

Lunar distance can be measured by measuring its parallax with respect to the star background. If you have friends around the globe, you can take pictures at the same time from various places, and measure the parallax directly. But people with no distant friends can do the measurement too. You just have to do a bit of extra maths.

The idea is to measure the parallax at two points in time in the same night, and then subtracting the parallax caused by lunar orbital motion.

The greatest parallax velocity caused by Earth's rotation will be observable when the moon is at its highest point in the sky. We will, therefore, do the measurement around that time.

Lunar parallax caused by orbital motion $p_o$ is

$$p_{o}=\frac{2\pi}{27.3\times24\,\textrm{h}}\frac{180°}{\pi}=0.55°/h.$$

Lunar parallax caused by earth rotation is, near the apex,

$$p_{e}=\frac{r}{d}\,\frac{\pi}{12\,\textrm{h}}\,\cos\frac{\pi\,l}{180°},$$

where $r$ is the Earth radius, $d$ is the distance to the moon, and $l$ is the observer latitude in degrees. Substituting these, we get

$$p_{e}=0.243°\textrm{h}^{-1}\,\cos\frac{\pi\,l}{180°}.$$

For Prague, for example, that is

$$p_{e}=0.156°\textrm{h}^{-1}.$$

----

If we were to observe the moon from Prague for 2h around its apex, we would expect to see orbital parallax of $1.10°$, which is about 2 lunar diameters. The parallax caused by Earth rotation would be $0.312°$, which is 40% of the lunar diameter. These two subtract, therefore the total observed parallax would be $0.788°$, roughly 1.6 lunar diameters.

From the observed parallax, we could calculate the lunar distance. If $p_{2h}$ is the observed 2-hour parallax, then

$$\frac{d}{r}=\frac{30°}{1.10°-p_{2h}}\,\cos\frac{\pi\,l}{180°}$$.

For Prague, again, that is

$$\frac{d}{r}=\frac{19.3°}{1.10°-p_{2h}}.$$
