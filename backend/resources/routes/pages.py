import flask


def index() -> str:
    return """
    <script>
        document.title = "Index";
    </script>
    <h1>Index</h1>
    <p>Index page</p>
    <p style="color: red;">This is a test</p>
    <p style="color: blue;">This is a test</p>
    <p style="color: green;">This is a test</p>
    <p style="color: yellow;">This is a test</p>
    <p style="color: orange;">This is a test</p>
    """
