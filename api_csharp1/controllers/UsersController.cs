using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using UsersApi.Models;
using UsersApi.Data;

[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly AppDbContext _context;

    public UsersController(AppDbContext context)
    {
        _context = context;
    }

    // GET api/users
    [HttpGet]
    public async Task<ActionResult<IEnumerable<User>>> GetUsers()
    {
        return await _context.Users.ToListAsync();
    }

    // GET api/users/{id}
    [HttpGet("{id}")]
    public async Task<ActionResult<User>> GetUser(int id)
    {
        var user = await _context.Users.FindAsync(id);

        if (user == null) return NotFound();

        return user;
    }

    // POST api/users
    [HttpPost]
    public async Task<ActionResult<User>> CreateUser(User user)
    {
        _context.Users.Add(user);
        await _context.SaveChangesAsync();

        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
    }

    // PUT api/users/{id}
    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateUser(int id, User updatedUser)
    {
        var user = await _context.Users.FindAsync(id);
        if (user == null) return NotFound();

        // Atualiza só os campos que podem mudar
        user.Name = updatedUser.Name;
        user.Email = updatedUser.Email;
        user.UserName = updatedUser.UserName;
        user.Password = updatedUser.Password;

        await _context.SaveChangesAsync();

        return Ok(user);
    }

    // DELETE api/users/{id}
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteUser(int id)
    {
        var user = await _context.Users.FindAsync(id);

        if (user == null) return NotFound();

        _context.Users.Remove(user);
        await _context.SaveChangesAsync();

        return NoContent();
    }
}
