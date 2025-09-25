def create_profile_html(name: str, age: int, location: str) -> str:
    return f"""
    <html>
        <body>
            <h1>{name}</h1>
            <p>Age: {age}</p>
            <p>Location: {location}</p>
        </body>
    </html>
    """