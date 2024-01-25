from reactpy import component, html, run

@component
def AppMain():
    return html.div(
        html.h2('Hello, World!')
    )

# python usage.py

if __name__ == "__main__":
    run(AppMain)
