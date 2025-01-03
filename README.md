# rCheck2

A tool to check if your program does not include unwanted functions.

## Description

This program allows you to detect specific functions in a program, based on specific rules.
You can choose for each function (using regular expressions), if you want to ban them or allow them.
By default, every function is allowed.

## Installation

```shell
curl -B https://raw.githubusercontent.com/Charlito33/rCheck2/refs/heads/master/install.sh | bash
```

## Features

* Very configurable.
* Full RegEx support.

## Limitations

* Program in entirely based on the ``nm`` command.
* Library detection is based on ``symbol@version`` output, with version being detected as the library.

## Usage

### Program arguments

```shell
./rcheck2 
```

### Rules examples

The program does not support JSON with comments, this is only for demonstration purposes.

#### Ban ``printf``

```json5
{
  "rules": [
    {
      "library": "GLIBC.*",
      "ban": [
        "printf"
      ]
    }
  ]
}
```

#### Ban every CSFML functions

```json5
{
  "rules": [
    {
      // CSFML is not detected in a library.
      "ban": [
        "sf.*_.*"
      ]
    }
  ]
}
```

#### Ban ``main`` function

```json5
{
  "rules": [
    {
      // If you don't specify "library", the program will only ban functions that are not in a library.
      "ban": [
        "main"
      ]
    }
  ]
}
```

#### Ban every functions

```json5
{
  "rules": [
    {
      "library": ".*", // Apply to any library
      "ban": [
        ".*" // Ban every function
      ]
    }
  ]
}
```

#### Only allow ``main`` function

(This will also ban GCC auto-generated functions).

```json5
{
  "rules": [
    {
      "library": ".*", // Apply to any library
      "ban": [
        ".*" // Ban every function
      ]
    },
    {
      "allow": [
        "main" // Only allow main that is not in a library
      ]
    }
  ]
}
```

#### Use unmodified RegEx

You may want to remove the ``^`` and ``$`` added to your RegEx expressions.
To do that, you just need to update the configuration.

```json5
{
  "configuration": {
    "extended_regex": true // Remove the '^' prefix and '$' suffix.
  },
  // ...
}
```

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/Charlito33/rCheck2">rCheck2</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/Charlito33">Charles Mahoudeau</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-SA 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt=""></a></p>
