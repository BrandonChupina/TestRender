from flask import Flask, request, jsonify
import csv
app = Flask(__name__)

class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
    def _height(self, node):
        if not node:
            return 0
        return node.height

    def _balance(self, node):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))

        return y

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))

        return y

    def insert(self, key, data):
        def _insert(node, key, data):
            if not node:
                return Node(key, data)
            
            if key < node.key:
                node.left = _insert(node.left, key, data)
            else:
                node.right = _insert(node.right, key, data)

            node.height = 1 + max(self._height(node.left), self._height(node.right))

            balance = self._balance(node)

            if balance > 1 and key < node.left.key:
                return self._rotate_right(node)

            if balance < -1 and key > node.right.key:
                return self._rotate_left(node)

            if balance > 1 and key > node.left.key:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

            if balance < -1 and key < node.right.key:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

            return node

        self.root = _insert(self.root, key, data)

    def search(self, key):
        def _search(node, key):
            if not node or node.key == key:
                return node
            if key < node.key:
                return _search(node.left, key)
            return _search(node.right, key)

        return _search(self.root, key)

tree = AVLTree()

@app.route('/bulk_upload', methods=['POST'])
def bulk_upload():
    file = request.files['file']
    if file.filename.endswith('.csv'):
        records = csv.reader(file)
        for row in records:
            key = int(row[0])
            data = row[1:]      
            tree.insert(key, data)
        return jsonify({'message': 'Bulk upload successful'})
    else:
        return jsonify({'error': 'Invalid file format'})

@app.route('/insert', methods=['POST'])
def manual_insert():
    key = int(request.json['key'])
    data = request.json['data']
    tree.insert(key, data)
    return jsonify({'message': 'Record inserted successfully'})

@app.route('/search/<int:key>', methods=['GET'])
def search_record(key):
    node = tree.search(key)
    if node:
        return jsonify({'data': node.data})
    else:
        return jsonify({'error': 'Record not found'})

@app.route('/group_info', methods=['GET'])
def group_info():
    info = {
        'members': [
            {'name': 'Brandon', 'ID': '001', 'contribution': 'Backend development'},
            {'name': 'Augusto', 'ID': '002', 'contribution': 'Frontend development'},
            {'name': 'Cesar', 'ID': '003', 'contribution': 'API design'},
        ]
    }
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)