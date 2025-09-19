# Fractal Generator
## Chaos Fractal
A chaos fractal is a type of fractal generator where a random point is chosen and then manipulated to create the fractal. It will randomly pick one vertex and move a given amount (Contraction factor) towards it. That pixel is saved, and then the point picks the next vertex. This process repeats until the full fractal is generated.
chaos_fractal.py is a generator script that will offer several prompts to make a custom chaos fractal.
  -Number of Vertices: The number of vertices or corners that the resultant fractal will have.
  -Custom Fractal? ('Yes' or 'No') If "Yes", it allows you to further customize the creation settings for the fractal. Otherwise ("No"), the default values will be selected
  -Contraction factor (0-1): Determines how close to the chosen vertex the point will move (0 - doesn't move, 1 - goes to the vertex, 0.5 is the default)
  -Allow consecutive repeats? (True/False): Determines whether or not the same vertex can be chosen multiple times in a row (if True, then it can repeat). Note: Answer must start with a capital "T" or "F" (Default     is True)
  -Custom Weights ('Yes' or 'No'): Allows you to make one vertex more likely to be chosen than another. Doesn't change much if allowed to run for a while, but has a visible difference at the beginning. (Default is     No)
    -Enter vertex weights separated by commas, or type 'random': Allows you to enter weights as a list (n1,n2,n3 with no spaces) or allow it to create random values (default is 1)
