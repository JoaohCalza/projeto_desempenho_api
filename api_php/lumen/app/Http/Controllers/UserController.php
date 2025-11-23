<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class UserController extends Controller
{
    // ===============================================
    // CREATE - POST /users
    // ===============================================
    public function create(Request $request)
    {
        $this->validate($request, [
            'name'     => 'required',
            'email'    => 'required|email|unique:users',
            'user'     => 'required|unique:users',
            'password' => 'required'
        ]);

        $user = User::create([
            'name'     => $request->name,
            'email'    => $request->email,
            'user'     => $request->user, // campo de login
            'password' => password_hash($request->password, PASSWORD_DEFAULT)
        ]);

        return response()->json($user, 201);
    }

    // ===============================================
    // READ ALL - GET /users
    // ===============================================
    public function index()
    {
        return response()->json(User::all());
    }

    // ===============================================
    // READ ONE - GET /users/{id}
    // ===============================================
    public function show($id)
    {
        $user = User::find($id);

        if (!$user)
            return response()->json(['error' => 'Not found'], 404);

        return response()->json($user);
    }

    // ===============================================
    // UPDATE - PUT /users/{id}
    // ===============================================
    public function update(Request $request, $id)
    {
        $user = User::find($id);

        if (!$user)
            return response()->json(['error' => 'Not found'], 404);

        // Validação para email e user únicos, ignorando o próprio ID
        $this->validate($request, [
            'email' => 'email|unique:users,email,' . $user->id,
            'user'  => 'unique:users,user,' . $user->id 
        ]);

        // atualiza os campos permitidos
        $user->update($request->only(['name', 'email', 'user']));

        // se enviar nova senha, atualiza
        if ($request->password) {
            $user->password = password_hash($request->password, PASSWORD_DEFAULT);
            $user->save();
        }

        return response()->json($user);
    }

    // ===============================================
    // DELETE - DELETE /users/{id}
    // ===============================================
    public function delete($id)
    {
        $user = User::find($id);

        if (!$user)
            return response()->json(['error' => 'Not found'], 404);

        $user->delete();

        return response()->json(['message' => 'Deleted']);
    }
}
