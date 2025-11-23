<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Hash;

class User extends Model
{
    protected $table = 'users';

    protected $fillable = [
        'name',
        'email',
        'user',
        'password',
    ];

    protected $hidden = [
        'password',
    ];

    /**
     * Hash automático da senha ao salvar no banco
     */
    public function setPasswordAttribute($value)
    {
        // Só faz hash se não estiver hashado ainda
        if (strlen($value) < 60 || !str_starts_with($value, '$2y$')) {
            $this->attributes['password'] = Hash::make($value);
        } else {
            $this->attributes['password'] = $value;
        }
    }
}
