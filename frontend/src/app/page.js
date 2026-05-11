"use client";
import { logoutUser } from "../../utils/auth";
import { useState } from "react";

export default function Home() {
  const [user, setUser] = useState(null);

  const handleLogout = async () => {
    await logoutUser();
  };

  return (
    <div className="min-h-screen bg-gray-100 items-center flex flex-col justify-center">
      {user ? <h1>Hi, {user.username}</h1> : <h1>Welcome stranger!</h1>}
      <button className="bg-blue-400 p-1 rounded-sm m-1" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
}
