import React, { useState, useCallback } from 'react';
import { Upload, FileText, Image, Code, File, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

const FileUploader = ({ onFilesSelected, disabled = false }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploadProgress, setUploadProgress] = useState({});

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  }, []);

  const handleChange = useCallback((e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  }, []);

  const handleFiles = (files) => {
    const fileArray = Array.from(files);
    setSelectedFiles(prev => [...prev, ...fileArray]);
    
    // Simulate upload progress
    fileArray.forEach((file, index) => {
      const fileId = `${file.name}-${Date.now()}-${index}`;
      setUploadProgress(prev => ({ ...prev, [fileId]: 0 }));
      
      // Simulate progress
      const interval = setInterval(() => {
        setUploadProgress(prev => {
          const currentProgress = prev[fileId] || 0;
          if (currentProgress >= 100) {
            clearInterval(interval);
            return prev;
          }
          return { ...prev, [fileId]: currentProgress + 10 };
        });
      }, 200);
    });

    if (onFilesSelected) {
      onFilesSelected(files);
    }
  };

  const removeFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const getFileIcon = (file) => {
    const extension = file.name.split('.').pop().toLowerCase();
    
    if (['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp'].includes(extension)) {
      return <Image className="h-4 w-4" />;
    } else if (['js', 'jsx', 'ts', 'tsx', 'html', 'css', 'json'].includes(extension)) {
      return <Code className="h-4 w-4" />;
    } else if (['txt', 'md', 'doc', 'docx'].includes(extension)) {
      return <FileText className="h-4 w-4" />;
    }
    return <File className="h-4 w-4" />;
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="space-y-6">
      {/* Upload Zone */}
      <Card className={`transition-all duration-200 ${
        dragActive ? 'border-primary bg-primary/5' : 'border-dashed border-2'
      } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:border-primary/50'}`}>
        <CardContent className="p-12">
          <div
            className="text-center"
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <Upload className={`mx-auto h-12 w-12 mb-4 ${
              dragActive ? 'text-primary' : 'text-muted-foreground'
            }`} />
            <h3 className="text-lg font-semibold mb-2">
              {dragActive ? 'Drop files here' : 'Drag and drop files here'}
            </h3>
            <p className="text-muted-foreground mb-4">
              or click to browse your computer
            </p>
            <input
              type="file"
              multiple
              onChange={handleChange}
              disabled={disabled}
              className="hidden"
              id="file-upload"
            />
            <Button asChild disabled={disabled}>
              <label htmlFor="file-upload" className="cursor-pointer">
                Choose Files
              </label>
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Selected Files */}
      {selectedFiles.length > 0 && (
        <Card>
          <CardContent className="p-6">
            <h4 className="font-semibold mb-4">Selected Files ({selectedFiles.length})</h4>
            <div className="space-y-3">
              {selectedFiles.map((file, index) => {
                const fileId = `${file.name}-${Date.now()}-${index}`;
                const progress = uploadProgress[fileId] || 0;
                
                return (
                  <div key={index} className="flex items-center space-x-3 p-3 border rounded-lg">
                    <div className="flex-shrink-0">
                      {getFileIcon(file)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-1">
                        <p className="text-sm font-medium truncate">{file.name}</p>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removeFile(index)}
                          className="h-6 w-6 p-0"
                        >
                          <X className="h-3 w-3" />
                        </Button>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge variant="secondary" className="text-xs">
                          {formatFileSize(file.size)}
                        </Badge>
                        {progress < 100 && (
                          <div className="flex-1">
                            <Progress value={progress} className="h-1" />
                          </div>
                        )}
                        {progress === 100 && (
                          <Badge variant="default" className="text-xs">
                            Ready
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default FileUploader;

