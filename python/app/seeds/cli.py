"""
CLI for database seeding operations using Typer
"""
import typer
import logging
from typing import Optional
from .manager import get_seed_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = typer.Typer(help="Database seeding CLI for BloggingApp")


@app.command()
def up(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """
    Seed the database with sample data (idempotent).
    
    This command will create sample users, posts, and comments.
    It's safe to run multiple times as it checks for existing data.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    typer.echo("🌱 Seeding database...")
    
    try:
        manager = get_seed_manager()
        success = manager.seed_up()
        
        if success:
            typer.echo("✅ Database seeded successfully!")
            typer.echo("\n📝 Sample credentials:")
            typer.echo("  Admin: admin / admin123")
            typer.echo("  Editor: editor / editor123") 
            typer.echo("  User: user1 / user123")
        else:
            typer.echo("❌ Database seeding failed!")
            raise typer.Exit(1)
            
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(1)


@app.command()
def down(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """
    Clear all seeded data from the database.
    
    This will remove sample users (except admin), posts, and comments
    that were created by the seeders.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Confirm destructive action
    confirm = typer.confirm("⚠️  This will delete seeded data. Continue?")
    if not confirm:
        typer.echo("Operation cancelled.")
        raise typer.Exit()
    
    typer.echo("🧹 Clearing seeded data...")
    
    try:
        manager = get_seed_manager()
        success = manager.seed_down()
        
        if success:
            typer.echo("✅ Seeded data cleared successfully!")
        else:
            typer.echo("❌ Data clearing failed!")
            raise typer.Exit(1)
            
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(1)


@app.command()
def reset(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """
    Clear existing seeded data and re-seed the database.
    
    This is equivalent to running 'seed down' followed by 'seed up'.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Confirm destructive action
    confirm = typer.confirm("⚠️  This will clear and re-seed data. Continue?")
    if not confirm:
        typer.echo("Operation cancelled.")
        raise typer.Exit()
    
    typer.echo("🔄 Resetting database...")
    
    try:
        manager = get_seed_manager()
        success = manager.seed_reset()
        
        if success:
            typer.echo("✅ Database reset completed!")
            typer.echo("\n📝 Sample credentials:")
            typer.echo("  Admin: admin / admin123")
            typer.echo("  Editor: editor / editor123")
            typer.echo("  User: user1 / user123")
        else:
            typer.echo("❌ Database reset failed!")
            raise typer.Exit(1)
            
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(1)


@app.command()
def demo(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """
    Seed the database with demo data for showcasing the application.
    
    Creates comprehensive sample data suitable for demonstrations.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    typer.echo("🎭 Seeding demo data...")
    
    try:
        manager = get_seed_manager()
        success = manager.seed_demo()
        
        if success:
            typer.echo("✅ Demo data seeded successfully!")
            typer.echo("\n📝 Demo credentials:")
            typer.echo("  Admin: admin / admin123")
            typer.echo("  Editor: editor / editor123")
            typer.echo("  User: user1 / user123")
            typer.echo("\n🎉 Ready for demo!")
        else:
            typer.echo("❌ Demo seeding failed!")
            raise typer.Exit(1)
            
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(1)


@app.command()
def status():
    """
    Show seeding status and what data exists.
    """
    from app.database.connection import SessionLocal
    from app.models.user import User
    from app.models.blog_post import BlogPost
    from app.models.comment import Comment
    
    typer.echo("📊 Database seeding status:")
    
    try:
        db = SessionLocal()
        
        # Count records
        user_count = db.query(User).count()
        post_count = db.query(BlogPost).count()
        comment_count = db.query(Comment).count()
        
        typer.echo(f"  Users: {user_count}")
        typer.echo(f"  Posts: {post_count}")
        typer.echo(f"  Comments: {comment_count}")
        
        # Check for seeded users
        admin = db.query(User).filter(User.username == "admin").first()
        editor = db.query(User).filter(User.username == "editor").first()
        user1 = db.query(User).filter(User.username == "user1").first()
        
        typer.echo("\n👥 Seeded users:")
        typer.echo(f"  Admin: {'✅' if admin else '❌'}")
        typer.echo(f"  Editor: {'✅' if editor else '❌'}")
        typer.echo(f"  User1: {'✅' if user1 else '❌'}")
        
        db.close()
        
    except Exception as e:
        typer.echo(f"❌ Error checking status: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
