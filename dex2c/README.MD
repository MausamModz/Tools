<a name="readme-top"></a>

<div align="center">
  <h1 align="center">𝐃𝐞𝐱𝟐𝐂</h1>

```
pip3 install -r requirements.txt
```


<!-- TABLE OF CONTENTS -->
<details>
<summary>Table of contents</summary>
  <ol>
    <li>
      <a href="#usage">Usage</a>
        <ul>
          <li><a href="#filters">Filters</a></li>
          <li><a href="#protect-apps">Protect apps</a></li>
        </ul>
    </li>
    <li><a href="#how-to-change-lib-name">How to change lib name</a></li>
  </ol>
</details>

<!-- USAGE EXAMPLES -->
# Usage

### Filters

Add all your filters in `filter.txt` file - one rule for each line. Filters are made using regex patterns. There are two types of filters available in **Dex2c** - whitelist, and blacklist. You can use them whenever you need them.

#### WhiteList

- Protect just one method in a specific class.
```
com/some/class;some_method(some_parameters)return_type
```

- Protect all methods in a specific class.
```
com/some/class;.*
```

- Protect all methods in all classes under a package path.
```
com/some/package/.*;.*
```

- Protect a method with the name onCreate in all classes.
```
.*;onCreate\(.*
```

#### BlackList

Adding an exclamation `!` sign before a rule will mark that rule as a blacklist.

- Exclude one method in a specific class from being protected.
```
!com/some/class;some_method(some_parameters)return_type
```

- Exclude all methods in a specific class from being protected.
```
!com/some/class;.*
```

- Exclude all methods in all classes under a package path from being protected.
```
!com/some/package/.*;.*
```

- Exclude a method with the name onCreate in all classes from being protected.
```
!.*;onCreate\(.*
```


### Protect apps

- Copy your apk file to `dex2c` folder where `dcc.py` is located and run this command.

```bash
python3 dcc.py -a input.apk -o output.apk
```

- Run this command to know about all the other options available in dcc to find the best ones for your needs.

```bash
python3 dcc.py --help
```


<!-- CHANGE LIB NAME -->
# How to change lib name

Open `project/jni/Android.mk` file in the cloned directory. You will find a variable named `LOCAL_MODULE`, initially with the value `stub`. Please change it to your desired lib name. Keep in mind the following instructions to prevent possible errors.
- Don't use spaces in lib name, use hyphen `-` or underscore `_`
- Don't use any kind of symbols or punctuations in lib name other than underscores and hyphens
- Don't start the lib name with the text `lib` itself



<!-- ROADMAP -->
# Roadmap

- [x] Add custom lib loader
- [x] Add new apksigner
- [x] Add multi-dex support
- [x] Add app abi handler
- [x] Add new options
    - [x] --skip-synthetic
    - [x] --custom-loader
    - [x] --force-keep-libs
    - [x] --obfuscate
