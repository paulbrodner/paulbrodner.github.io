---
layout: post
title: WebBrowser Testing using standalone docker images
date: 2018-03-29 13:00 +0300
tags: [Java, docker, docker-compose, selenium-standalone]
description: Step by step guide to configure your selenium tests to run remotely on a standalone docker container
---

If you just want to run your Selenium tests seamlessly without too many configuration like 
* setting up a [Selenium Hub](https://github.com/SeleniumHQ/selenium/wiki/Grid2)
* configure [nodes](https://github.com/SeleniumHQ/selenium/wiki/Grid2) with appropriate Browser Types (Chrome, Firefox, etc)

then you can easily start using the official [Docker Images](https://hub.docker.com/r/selenium/) for [Selenium Grid Server](https://github.com/SeleniumHQ/docker-selenium). 

{% include idea.html content="If you want to skip the description bellow, just follow the <a href='https://github.com/paulbrodner/headless-browser-testing/blob/master/README.md' target='_blank'>Quick Steps</a> guide from <a href='https://github.com/paulbrodner/headless-browser-testing' target='_blank'>headless-browser-testing</a> repo." %}

### Sample project: running selenium tests in java

1) I've created [headless-browser-testing](https://github.com/paulbrodner/headless-browser-testing) repository where I defined a standard [SpringBot app](https://projects.spring.io/spring-boot/) with selenium firefox dependency for now:
```java
		<dependency>
			<groupId>org.seleniumhq.selenium</groupId>
			<artifactId>selenium-firefox-driver</artifactId>
		</dependency>
```
[This is a starter app that I am using to test the docker standalone selenium images]

2) I am using the [Factory patttern](https://github.com/paulbrodner/headless-browser-testing/blob/master/src/main/java/com/paulbrodner/headlessbrowsertesting/WebDriverFactory.java#L16) to define the WebDriver that will run my test.
```java
@Service
public class WebDriverFactory implements FactoryBean<WebDriver> {

  @Override
  public WebDriver getObject() throws Exception {
    Capabilities capabilities = fromWebDriverBrowserName(webdriverBrowserName);
    
    WebDriver driver = new RemoteWebDriver(webdriverHubUrl, capabilities);
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    
    return driver;
  }
}
```

Here I am defining how the WebDriver is constructed with the [RemoteWebDriver](https://github.com/paulbrodner/headless-browser-testing/blob/master/src/main/java/com/paulbrodner/headlessbrowsertesting/WebDriverFactory.java#L28) object (the WebDriver browser name is defined in the [application.properties](https://github.com/paulbrodner/headless-browser-testing/blob/master/src/main/resources/application.properties#L3) file).


3) In the test package of my project, I am [@Autowire](https://github.com/paulbrodner/headless-browser-testing/blob/master/src/test/java/com/paulbrodner/headlessbrowsertesting/HeadlessBrowserTestingApplicationTests.java#L23) the WebDriverFactory defined above. 

This will:
* initialize the browser
* open google page
* get a screenshot
* and assert title is correct

```java
@Test
public void ableToOpenGooglePage() throws Exception {
    driver = driverFactory.getObject();
    driver.get("http://www.google.com");

    WebDriver augmentedDriver = new Augmenter().augment(driver); 		
    File source = ((TakesScreenshot)augmentedDriver).getScreenshotAs(OutputType.FILE);        
    FileUtils.copyFile(source, new File("./target", source.getName())); 
    
    assertEquals("Google", driver.getTitle());
}
```

4) running the tests will fail at this time if you don't have a Selenium Grid configured at 'http://localhost:4444/wd/hub' as we specified on [application.properties](https://github.com/paulbrodner/headless-browser-testing/blob/master/src/main/resources/application.properties) file.

### Start the docker standalone images

1) I am using [docker-compose](https://github.com/paulbrodner/headless-browser-testing/blob/master/docker-compose.yml) to start up a new firefox standalone instance.
```ruby
version: "2"
services:    
  standalone-firefox:
     image: selenium/standalone-firefox:3.11      
     ports:
       - 4444:4444
       - 5900:5900
```

I am pulling the official 'selenium/standalone-firefox:3.11' image and start it locally on ports 4444 and 5900 (vnc port)

This will start a grid on `localhost:4444/wd/hub` and also make available Firefox inside the same container.

2) In the root folder you will find a [start-selenium.sh](https://github.com/paulbrodner/headless-browser-testing/blob/master/start-selenium.sh) helper script that will
execute the docker-compose and wait for the hub to start.
