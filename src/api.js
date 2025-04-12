export const API_URL = "http://localhost:8000/api";

export async function getCSRFToken() {
    try {
        const response = await fetch(`${API_URL}/csrf-token`, { credentials: "include" });
        if (response.ok) {
            const data = await response.json();
            return data.csrfToken;
        } else {
            console.error("Failed to fetch CSRF token:", response.statusText);
            return { error: "Failed to fetch CSRF token" };
        }
    } catch (error) {
        console.error("Error fetching CSRF token:", error);
        return { error: "Network error" };
    }
}

export async function register(username, password) {
    try {
        const response = await fetch(`${API_URL}/user`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            return { error: error.error };
        }
    } catch (error) {
        console.error("Error registering user:", error);
        return { error: "Network error" };
    }
}

export async function login(username, password) {
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            return { error: error.error };
        }
    } catch (error) {
        console.error("Error logging in:", error);
        return { error: "Network error" };
    }
}

export async function logout() {
    try {
        const response = await fetch(`${API_URL}/logout`, {
            method: "POST",
            credentials: "include",
        });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            return { error: error.error };
        }
    } catch (error) {
        console.error("Error logging out:", error);
        return { error: "Network error" };
    }
}

export async function checkSession() {
    try {
        const response = await fetch(`${API_URL}/session`, {
            method: "GET",
            credentials: "include",
        });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            return { error: error.error };
        }
    } catch (error) {
        console.error("Error checking session:", error);
        return { error: "Network error" };
    }
}


// export async function getUser() {
//     try {
//         const response = await fetch(`${API_URL}/user`, { credentials: "include" });

//         if (response.ok) {
//             return await response.json();
//         } else {
//             const error = await response.json();
//             return { error: error.error };
//         }
//     } catch (error) {
//         console.error("Error fetching user:", error);
//         return { error: "Network error" };
//     }
// }

export async function getMessages() {
    try {
        const response = await fetch(`${API_URL}/message`, { credentials: "include" });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            return { error: error.error };
        }
    } catch (error) {
        console.error("Error fetching messages:", error);
        return { error: "Network error" };
    }
}

export async function sendMessage(content) {
    try {
        const response = await fetch(`${API_URL}/message`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ content }),
        });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            return { error: error.error };
        }
    } catch (error) {
        console.error("Error sending message:", error);
        return { error: "Network error" };
    }
}

export async function deleteMessage(id) {
    try {
        const response = await fetch(`${API_URL}/message/${id}`, {
            method: "DELETE",
            credentials: "include",
        });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            return { error: error.error };
        }
    } catch (error) {
        console.error("Error deleting message:", error);
        return { error: "Network error" };
    }
}

export async function uploadProfilePicture(file) {
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        credentials: "include",
        body: formData,
      });
  
      if (response.ok) {
        return await response.json(); // Return the server's response
      } else {
        const error = await response.json();
        return { error: error.error };
      }
    } catch (error) {
      console.error("Error uploading profile picture:", error);
      return { error: "Network error" };
    }
  }

