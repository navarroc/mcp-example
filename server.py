from fastmcp import FastMCP
import sqlite3
import os

mcp = FastMCP("Example MCP Server")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "samples.db")

def init_db():
    """ Create a sample database if it doesn't exist"""
    with sqlite3.connect(DB_PATH) as db_conn:
        db_conn.execute("CREATE TABLE IF NOT EXISTS crops (id INTEGER PRIMARY KEY, name TEXT, long_name TEXT, unit TEXT, ref_price REAL)")
        db_conn.execute("DELETE FROM crops")
        db_conn.execute("INSERT INTO crops (name, long_name, unit, ref_price) VALUES('corn', 'Corn', 'bu/acre', "
                        "3.70 ), ('soybeans', 'Soybeans', 'bu/acre', 8.40 ), ('wheat', 'Wheat', 'bu/acre', 5.50 )")

@mcp.tool()
def list_tables() -> list[str]:
    """List all available tables in the database"""
    with sqlite3.connect(DB_PATH) as db_conn:
        cursor = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in cursor.fetchall()]

@mcp.tool()
def query_crop_by_name(name: str) -> str:
    """
    Search for a crop by its name
    Use '%' as a wildcard (e.g., 'Co%' for Corn).
    To list all crops, pass '%' as the name.
    """
    with sqlite3.connect(DB_PATH) as db_conn:
        cursor = db_conn.execute("SELECT * FROM crops WHERE name LIKE ?", (f"%{name}%",))
        results = cursor.fetchall()

        if not results:
            return f"No crops found matching '{name}'."

        return "\n".join([f"ID: {r[0]}, Name: {r[1]}, Long Name: {r[2]}, Unit: {r[3]}, Ref Price: ${r[4]}" for r in
                          results])

@mcp.tool()
def get_weather(city: str) -> dict:
    """Get the current weather for a city"""
    # This is where we'd add real logic - calling an API
    return {"city": city, "temp": 55, "condition": "sunny"}

@mcp.tool()
def add_numbers(val1: int, val2: int) -> int:
    """Add two numbers and return the sum"""
    # This is where we'd add real logic - calling an API
    return val1 + val2

@mcp.resource("status://current")
def get_system_status() -> str:
    """Provides a static system status report."""
    return "All systems operational. Connection: HTTP/SSE."

if __name__ == "__main__":
    init_db()
    mcp.run()
    # Uncomment this if you want to use HTTP/SSE
    #mcp.run(transport="sse")
