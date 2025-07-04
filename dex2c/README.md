<h1>Dex2C</h1>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Poppins&size=15&duration=6000&pause=500&color=D8F748&width=700&lines=Method-based+AOT+compiler+that+can+wrap+Dalvik+bytecode+with+JNI+native+code.)](https://git.io/typing-svg)

Forked from Kirlif/[d2c](https://github.com/Kirlif/d2c)

### Requierements
1. Python3
2. lxml python package.
   ```bash
   pkg install python-lxml
   ```
   or
   ```bash
   pip3 install -U --user 'lxml>=4.3.0'
   ```
   on Termux:
      ```bash
   pkg install libxml2 libxslt
   CFLAGS="-O0" pip install -U lxml
   ```
3. JRE/JDK
3. Android NDK

### Installation
   ```bash
   git clone https://github.com/MausamModz/Tools.git
   ```
- configure dcc.cfg with your NDK path

<!-- USAGE EXAMPLES -->
# Usage

### Filters

Add all your filters in `filter.txt` file - one rule for each line. Filters are made using regex patterns. There are two types of filters available in **Dex2c** - whitelist, and blacklist. You can use them whenever you need them.

#### WhiteList

- Protect just one method in a specific class.
```
com/some/class;some_method(some_parameters)return_type
```

- Protect OnCreate method (copy signature method)
```
com/example/test/MainActivity;onCreate\(Landroid/os/Bundle;\)V
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
python3 dcc.py -i input.apk

```

- Run this command to know about all the other options available in dcc to find the best ones for your needs.

```bash
python3 dcc.py --help
```

### Major updates
- changed <a href="https://apktool.org/">Apktool</a> for <a href="https://github.com/REAndroid/APKEditor">APKEditor</a>
- cleaned androguard from useless parts and removed dependencies
- DEX file support: creates a ZIP archive of the built libraries and dex file
- skip constructors by default
- the application class is the loader ; if not defined or absent from dex, the custom loader is used
- --allow-init option: do not skip constructors
- --lib-name option: edit the library name, default: stub
- --output default value is « output.apk » for an APK else « output.zip » for a DEX
- --input only is required 
- all options can be configured in dcc.cfg ; options passed to the command line have priority
- adjust APP_PLATFORM automatically

### Settings

|  Cli  |  Config  |  Default  |
| ----- | -------- |  -------- |
|-i, --input|||
| -o, --output|output|output.(apk\|zip)|
|-p, --obfuscate|obfuscate|false|
|-d, --dynamic-register|dynamic_register|false|
|-s, --skip-synthetic|skip_synthetic|false|
|-a, --allow-init|allow_init|false|
|-k, --force-keep-libs|force_keep_libs|false|
|-b, --no-build|no_build|false|
|-f, --filter|filter|filter.txt|
|-c, --custom-loader|custom_loader|amimo.dcc.DccApplication|
|-r, --force-custom-loader|force_custom_loader|false
|-l, --lib-name|lib_name|stub|
|-e, --source-dir|source_dir||
|-z, --project-archive|project_archive|project-source.zip|
