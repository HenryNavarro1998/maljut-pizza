import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class JSONModel:
    def __init__(self, filename: str):
        self.filename = os.path.join('app', 'data', filename)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Asegura que el archivo JSON existe"""
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def _read_data(self) -> List[Dict[str, Any]]:
        """Lee los datos del archivo JSON"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Asegurar que los datos son una lista
                if not isinstance(data, list):
                    data = []
                # Asegurar que cada elemento es un diccionario
                data = [item for item in data if isinstance(item, dict)]
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write_data(self, data: List[Dict[str, Any]]):
        """Escribe los datos en el archivo JSON"""
        # Asegurar que los datos son una lista de diccionarios
        if not isinstance(data, list):
            data = []
        data = [item for item in data if isinstance(item, dict)]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todos los registros"""
        return self._read_data()
    
    def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un registro por su ID"""
        data = self._read_data()
        return next((item for item in data if isinstance(item, dict) and item.get('id') == id), None)
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo registro"""
        records = self._read_data()
        # Generar nuevo ID
        new_id = max([item.get('id', 0) for item in records if isinstance(item, dict)], default=0) + 1
        # Agregar ID y fecha de creación
        data['id'] = new_id
        data['created_at'] = datetime.utcnow().isoformat()
        records.append(data)
        self._write_data(records)
        return data
    
    def update(self, id: int, data: Dict[str, Any]) -> bool:
        """Actualiza un registro existente"""
        records = self._read_data()
        for i, record in enumerate(records):
            if isinstance(record, dict) and record.get('id') == id:
                # Mantener el ID y la fecha de creación
                data['id'] = id
                data['created_at'] = record.get('created_at')
                records[i] = data
                self._write_data(records)
                return True
        return False
    
    def delete(self, id: int) -> bool:
        """Elimina un registro"""
        records = self._read_data()
        for i, record in enumerate(records):
            if isinstance(record, dict) and record.get('id') == id:
                records.pop(i)
                self._write_data(records)
                return True
        return False 