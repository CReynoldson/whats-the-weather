# Welcome To What's The Weather - Your Friendly Neighbourhood Weather Buddy

## Notes
What's The Weather is built on Flask, a lightweight Python microframework. I chose Flask because it is quick to get up and running while providing multiple customization options. It also allowed me to block any HTTP methods other than GET requests on the weather route as a default, which saved development time. Since this is a small API proxy app I didn't feel the need to use a larger framework like Django. On the downside, Flask does not provide an out-of-the-box solution to production deployment, which I believe larger frameworks have.

Had I implemented a UI I would have used React to more easily handle front end data and user interactions than if I were using a static templating library like Jinja2. 

The bundle size for React would be larger than something like Jinja2 scripts, but I think it makes up for that by making the UX easier to implement, and the bundle size issue can be mitigated by chunking the packages and having an efficient webpack setup.

### Date
7 May 2021

### Location of deployed application
You can access What's The Weather [here](http://quiet-anchorage-65722.herokuapp.com) if you want to see a very boring index page, [here](http://quiet-anchorage-65722.herokuapp.com/v1/weather?city=Vancouver) for light-hearted lack-of-api-token shaming, and finally [here](http://quiet-anchorage-65722.herokuapp.com/v1/weather?city=Vancouver&app-token=PatrickIsPurrfect) to send an authenticated request.

**Or CURL it if you'd like:**

**Unathenticated Request**
`curl 'http://quiet-anchorage-65722.herokuapp.com/v1/weather?city=Vancouver'`

**Authenticated Request**
`curl 'http://quiet-anchorage-65722.herokuapp.com/v1/weather?city=Vancouver&app-token=PatrickIsPurrfect'`

Please note it's running on a hobby dyno so you may need to give it a moment to wake up!

Or, access it from the comfort of your own local installation by following the instructions below.

### Time spent
- 30 minutes planning (including overzealously plotting stretch work I then didn't have time to do)
- 40 minutes architecting and writing the server / routes / controller / service files
- 50 minutes proxying the weather API
- 1 hour revisiting server architecture and working with the proxy API
- 1 hour writing tests
- 1 hour adding data manipulation and error handling to the controller and route files
- 45 minutes adding files and environment config for deploying to Heroku 
- 1 hour writing the Readme because I'm the odd duck that enjoys writing documentation
- 30 minutes to add authentication handling with hardcoded variable
- 30 minutes review, bug fixing, general code cleanup

### Assumptions made
I assumed the use case for this data was focused on non-scientific users who just want to get a layperson's view of the weather. As a result I limited the precision of the temperature values to 2 decimal places, which would probably be too vague if that data were being used by meteorologists, statisticians, etc.

I also assumed that if the API didn't allow for requesting a specific temperature unit, the requester would like to get all 3 back and can filter their own data from there. 

### Shortcuts/Compromises made
My authentication stretch feature is more just an example of how authentication on routes could work in the app and is definitely not very secure. It is technically an authenticated route but the authentication token is the same for everyone, so this feature could be a lot more developed and robust. Having one token stored in the environment variables was a shortcut to have working authentication requirements without any unique token handling for different users. 

There is also some code that definitely assumes the only thing the API needs to search on is the city name since that was all I implemented (specifically the get_weather_by_city_name call in the controller's get_weather function). This was a shortcut so I didn't have to integrate potential other filters that the controller should also be able to handle in a production environment.

### Stretch goals attempted
The only stretch goal I wasn't able to attempt was building a simple UI for the API, but I sure did have ideas about that! I've included them in the section below.

I enjoyed proxying a real API for the weather data rather than making up weather at random, but lost some time there waiting for my API key to activate which I could have put to better use on other features. It also gave me a lot of ideas for how to iterate on my app, for example, integrating filters on temperature units, latitude and longitude, etc, which I would have liked to implement if I'd had the opportunity. I did attempt to build some of that handling into the app regardless as an indication of how those filters could be handled in the future.

Deploying to Heroku was straightforward, but I regret spending time figuring out how to run a 'production' server by integrating gunicorn. Normally that would make sense but since this is a small app that doesn't need to benefit from production-level processes I think that time could also have been better spent elsewhere.

### Instructions to run assignment locally
1. Clone this repository locally into the folder of your choosing

2. Create a virtual environment in that folder to avoid polluting your computer with global packages - [helpful, python-approved instructional article  here](https://docs.python.org/3/library/venv.html)

3. Once you're safely in your virtual environment, run `pip install -r requirements.txt` to download dependencies

4. Run the app with `python main.py` - please note, this app requires python3 so depending on your personal path set up you may need to run `python3 main.py` instead. You know how to get to python3 on your own computer better than I do, so I shan't tell you how to live your life. 

5. For maximum enjoyment and profit you will want to add `app-token=PatrickIsPurrfect` to your query parameters. Patrick is my cat and he walked across the keyboard often enough during this challenge that I felt he should be included in some way. So I made him the hard coded authentication token you need to use in order to access any of the weather data.


### What did you not include in your solution that you want us to know about?

I had planned to include a UI written in React that would allow users to dynamically search cities from a dropdown. 

The dropdown would be populated by a library (not sure which library; I'm making an assumption that one exists, but for the purposes of the app I could have seeded a few Canadian cities as a proof of concept).

I believe having a searchable dropdown selector would be an overall better user experience, and it would also help with data integrity issues inherint in the API filter. 

For example, what happens when a user searches the API with just "Portland"? As it is currently, they get weather for both Portland Maine, and Portland Oregon. But which one did they want and how are they able to specify that more clearly without the ability to add additional filters? I think as a user I would prefer just the city I asked for, and not also one across the country that happens to have the same name. A drop down would help me avoid that. It would also help minimize user typos by prompting city options, rather than the user having to spell a city properly.


Results from the API included all 3 temperature units (see Assumptions for more detail), and I would have had the weather details displayed in a box under the city drop down, with tabs to toggle between the different unit views. Clicking a tab would re-render the box with that unit's temperature data.

A stretch goal for the stretch goal was to integrate a map using Leaflet or Mapbox and allow users to select a city or lat/long pair and call the weather API with that data, which I thought would be a fun feature.

