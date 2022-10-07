# cli

Main entrypoint for this dummy program

**Usage:**

```text
cli [OPTIONS] COMMAND [ARGS]...
```

**Options:**

```text
  --help  Show this message and exit.
```

**Subcommands**

- *bar*: The bar command
- *foo*: *No description was provided with this command.*

## bar

The bar command

**Usage:**

```text
cli bar [OPTIONS] COMMAND [ARGS]...
```

**Options:**

```text
  --help  Show this message and exit.
```

**Subcommands**

- *hello*: Simple program that greets NAME for a total of COUNT times.

### hello

Simple program that greets NAME for a total of COUNT times.

**Usage:**

```text
cli bar hello [OPTIONS]
```

**Options:**

```text
  --count INTEGER  Number of greetings.
  --name TEXT      The person to greet.
  --help           Show this message and exit.
```

## foo

**Usage:**

```text
cli foo [OPTIONS]
```

**Options:**

```text
  --help  Show this message and exit.
```
