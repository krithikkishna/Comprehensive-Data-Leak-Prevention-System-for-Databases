
const express = require('express');
const mysql = require('mysql2');
const path = require('path');

const app = express();
const port = 5501;

app.use(express.static(path.join(__dirname, '../frontend')));
app.use(express.urlencoded({ extended: true }));

const pool = mysql.createPool({
  host: '127.0.0.1', 
  user: 'root', 
  password: '',
  database: 'dataguard',           
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});
    
console.log('MySQL connection pool created successfully.');

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend', 'index.html'));
});

app.post('/submit-data', (req, res) => {
    const { regdno, name, email, branch } = req.body;
    const sql = 'INSERT INTO users (regdno, name, email, branch) VALUES (?, ?, ?, ?)';
    const values = [regdno, name, email, branch];

    pool.query(sql, values, (error, results) => {
        if (error) {
            console.error('Error saving data to MySQL:', error);
            if (error.code === 'ER_DUP_ENTRY') {
                return res.status(400).send('Error: Registration number or email already exists.');
            }
            return res.status(500).send('An error occurred while saving the data.');
        }
        console.log('Data saved successfully to MySQL. Insert ID:', results.insertId);
        res.status(201).send('Form submission successful!');
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
