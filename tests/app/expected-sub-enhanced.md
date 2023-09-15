# cli { #cli data-toc-label="cli" }

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

- *[bar](#cli-bar)*: The bar command
- *[foo](#cli-foo)*: *No description was provided with this command.*

## cli bar { #cli-bar data-toc-label="bar" }

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

- *[hello](#cli-bar-hello)*: Simple program that greets NAME for a total of COUNT times.

### cli bar hello { #cli-bar-hello data-toc-label="hello" }

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

## cli foo { #cli-foo data-toc-label="foo" }

**Usage:**

```text
cli foo [OPTIONS]
```

**Options:**

```text
  --help  Show this message and exit.
```
