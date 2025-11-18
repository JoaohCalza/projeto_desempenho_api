<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\UserController;

Route::get('/users', [UserController::class, 'index']);   // listar usuários
Route::post('/users', [UserController::class, 'store']);  // criar usuário
