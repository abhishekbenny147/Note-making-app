document.addEventListener("DOMContentLoaded", loadNotes);

function loadNotes() {
    fetch("/get_notes")
        .then(response => response.json())
        .then(data => {
            const notesList = document.getElementById("notes");
            notesList.innerHTML = "";
            data.notes.forEach((note, index) => {
                notesList.innerHTML += `
                    <li>
                        <span class="note-text">${note}</span>
                        <button onclick="editNote(${index})">Edit</button>
                        <button onclick="deleteNote(${index})">Delete</button>
                    </li>
                `;
            });
        });
}

function saveNote() {
    const note = document.getElementById("note").value;
    fetch("/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ note })
    }).then(response => response.json())
      .then(() => {
          document.getElementById("note").value = "";
          loadNotes();
      });
}

function editNote(index) {
    const newNote = prompt("Edit your note:");
    if (newNote) {
        fetch(`/update/${index}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ note: newNote })
        }).then(() => loadNotes());
    }
}

function deleteNote(index) {
    if (confirm("Are you sure you want to delete this note?")) {
        fetch(`/delete/${index}`, { method: "DELETE" })
            .then(() => loadNotes());
    }
}
