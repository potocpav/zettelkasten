---
date: 2021-07-11T09:55
tags:
  - astronomy
  - experiment
---

# Measuring Moon Distance

Lunar distance can be measured by measuring its motion with respect to the star background. If you have friends around the globe, you can take pictures of the moon against the star background at the same time from various places, and measure the difference in lunar positions directly. But people with no distant friends can do the measurement too. You just have to do a bit of extra maths.

The idea is to take a photo of moon and the stars twice during the same night, measure the difference in lunar positions, and subtract the part of difference caused by lunar orbital motion.

Observed motion will be influenced by Earth's rotation maximally when the moon is at its highest point in the sky. We will, therefore, do our measurements around that time. This is also convenient because it simplifies the maths greatly.

Apparent lunar motion caused by lunar orbital motion $p_o$ is, assuming a circular orbit:

$$p_{o}=\frac{2\pi}{27.3\times24\,\textrm{h}}\frac{180°}{\pi}=0.55°/h.$$

Apparent lunar motion caused by earth rotation $p_e$ is, near lunar [culmination](https://en.wikipedia.org/wiki/Culmination),

$$p_{e}=\frac{r}{d}\,\frac{\pi}{12\,\textrm{h}}\,\frac{180°}{\pi}\cos\frac{\pi\,l}{180°},$$

where $r$ is the Earth radius, $d$ is the distance to the moon, and $l$ is the observer latitude in degrees. Substituting these, we get

$$p_{e}=0.249°\textrm{h}^{-1}\,\cos\frac{\pi\,l}{180°}.$$

For Prague, for example, that is

$$p_{e}=0.160°\textrm{h}^{-1}.$$

If we disregard axial tilt and lunar orbital tilt, we can get the total apparent motion $p$ by subtracting the two contributions. Doing this can lead to an error of up to roughly 7% in $p$, or 20% in the computed distance.

$$p=p_o-p_e.$$

The biggest source of error is the fact that the lunar orbit is not circular. The real orbit is elliptical ($e \approx 0.055$), 
so the actual orbital motion rate varies between roughly 0.49 and 0.61°/h. Since we subtract this from a much smaller Earth-rotation signal, 
this alone can make the computed distance off by −30 % to +60 %. Without an ephemeris this error is hard to avoid, so the method gives the order of magnitude rather than a precise value.

## Example

If we were to observe the moon from Prague for 2h around its apex, we would expect to see apparent motion caused by lunar orbit of $1.10°$, which is about 2 lunar diameters. The apparent motion caused by Earth rotation would be $0.320°$, which is 60% of the lunar diameter. If we subtract these two, we get a total observed apparent motion of $0.78°$, roughly 1.5 lunar diameters.

This was assuming zero contribution of axial tilt. If we assume maximum tilt, we get the result of $0.82°$ by applying [the law of cosines](https://en.wikipedia.org/wiki/Law_of_cosines).

From the observed apparent motion, we could calculate the lunar distance. If $p_{2h}$ is the observed 2-hour apparent motion, then

$$\frac{d}{r}=\frac{30°}{1.10°-p_{2h}}\,\cos\frac{\pi\,l}{180°}.$$

For Prague, that is

$$\frac{d}{r}=\frac{19.2°}{1.10°-p_{2h}}.$$

We, again, disregarded the axial tilt.
