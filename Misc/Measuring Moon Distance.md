---
date: 2021-07-11T09:55
tags:
  - astronomy
  - experiment
---

# Measuring Moon Distance

Lunar distance can be measured by measuring its parallax with respect to the star background. If you have friends around the globe, you can take pictures of the moon against the star background at the same time from various places, and measure the parallax directly. But people with no distant friends can do the measurement too. You just have to do a bit of extra maths.

The idea is to measure the lunar parallax twice during the same night, and subtract the part of the parallax caused by lunar orbital motion.

Observed parallax will be influenced by Earth's rotation maximally when the moon is at its highest point in the sky. We will, therefore, do our measurements around that time. This is also convenient because it simplifies the maths greatly.

Lunar parallax caused by lunar orbital motion $p_o$ is

$$p_{o}=\frac{2\pi}{27.3\times24\,\textrm{h}}\frac{180°}{\pi}=0.55°/h.$$

Lunar parallax caused by earth rotation $p_e$ is, near lunar [culmination](https://en.wikipedia.org/wiki/Culmination),

$$p_{e}=\frac{r}{d}\,\frac{\pi}{12\,\textrm{h}}\,\cos\frac{\pi\,l}{180°},$$

where $r$ is the Earth radius, $d$ is the distance to the moon, and $l$ is the observer latitude in degrees. Substituting these, we get

$$p_{e}=0.243°\textrm{h}^{-1}\,\cos\frac{\pi\,l}{180°}.$$

For Prague, for example, that is

$$p_{e}=0.156°\textrm{h}^{-1}.$$

If we disregard axial tilt, we can get the total parallax $p$ by subtracting the two parallax contributions. Doing this can lead to the maximum error of roughly 10%.

$$p=p_o-p_e.$$

## Example

If we were to observe the moon from Prague for 2h around its apex, we would expect to see parallax caused by lunar orbit of $1.10°$, which is about 2 lunar diameters. The parallax caused by Earth rotation would be $0.312°$, which is 40% of the lunar diameter. If we subtract these two, we get a total observed parallax of $0.788°$, roughly 1.6 lunar diameters.

This was assuming zero contribution of axial tilt. If we assume maximum tilt, we get the result of $0.82°$ by applying [the law of cosines](https://en.wikipedia.org/wiki/Law_of_cosines).

From the observed parallax, we could calculate the lunar distance. If $p_{2h}$ is the observed 2-hour parallax, then

$$\frac{d}{r}=\frac{30°}{1.10°-p_{2h}}\,\cos\frac{\pi\,l}{180°}$$.

For Prague, that is

$$\frac{d}{r}=\frac{19.3°}{1.10°-p_{2h}}.$$

We, again, disregarded the axial tilt.
