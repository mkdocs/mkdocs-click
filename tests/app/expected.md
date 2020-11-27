# cli

Main entrypoint for this dummy program

Usage:

```
cli [OPTIONS] COMMAND [ARGS]...
```

## bar

The bar command

Usage:

```
cli bar [OPTIONS] COMMAND [ARGS]...
```

### hello

Simple program that greets NAME for a total of COUNT times.

Usage:

```
cli bar hello [OPTIONS]
```

**Options:**

| Option | Type | Description | Required | Default |
| ------ | ---- | ----------- | -------- | ------- |
| `--count` | INTEGER | Number of greetings. |  | `1` |
| `--name` | TEXT | The person to greet. |  |  |

## foo

Usage:

```
cli foo [OPTIONS]
```
