import sublime, sublime_plugin
import desktop
import tempfile
import markdown
import os


class MarkdownPreviewCommand(sublime_plugin.TextCommand):
	""" preview file contents with python-markdown and your web browser"""

	def run(self, edit, target='browser'):
		print edit, target
		region = sublime.Region(0, self.view.size())
		encoding = self.view.encoding()
		if encoding == 'Undefined':
			encoding = 'UTF-8'
		elif encoding == 'Western (Windows 1252)':
			encoding = 'windows-1252'
		else:
			encoding = 'UTF-8'
			
		contents = self.view.substr(region)

		# convert the markdown
		markdown_html = markdown.markdown(contents)

		# Get the File Path
		file_url = self.view.file_name()
				  
	   
		# Get the Markdown Preview Path		
		markdown_path = os.path.join(sublime.packages_path(), 'Markdown Preview')
		
		# output
		if target == 'browser':
			 
			# Build the Local Full Html
			html_contents = '<!DOCTYPE html>\n<html>\n<head>\n'
			html_contents += u'<meta charset="%s">\n' % encoding
			
			# Make the File Name to the Title
			file_basename = os.path.basename(file_url)  
			html_contents += u'<title>%s</title>\n' % file_basename
			
			# Local Style
			html_contents += u'<link href="file:///%s\markdown.css" type="text/css" rel="stylesheet" />\n' % markdown_path
			
			# Code Highligght Support
			html_contents += u'<link href="file:///%s\highlight\styles\googlecode.css" type="text/css" rel="stylesheet" />\n' % markdown_path
			html_contents += u'<script src="file:///%s\highlight\highlight.pack.js" type="text/javascript"></script>\n' % markdown_path
			html_contents += "<script>hljs.tabReplace = '  ';hljs.initHighlightingOnLoad();</script>\n"
			
			# LaTeX Support		
			html_contents += u'<script src="file:///%s\mathjax\MathJax.js?config=default" type="text/javascript"></script>\n</head>\n<body>\n' % markdown_path
			
			# Main Html
			html_contents += markdown_html
			
			html_contents += '\n</body>\n</html>'


			# Choose the Html File Path
			(file_path,file_suffix)=os.path.splitext(file_url)       
			
			if file_suffix == '.md':
				html_file_path = '%s.html' % file_path
				html_file = file(html_file_path,'w')
			elif file_suffix == '.markdn':
				file_path_html = os.path.dirname(file_url)
				html_file_path = '%s\\HTMLs' % file_path_html
				html_file_path += '\\%s.html' % file_basename
				html_file = file(html_file_path,'w')
			else:
				html_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
			
			html_file.write(html_contents.encode(encoding))
			html_file.close()
			desktop.open(html_file.name)
		elif target == 'sublime':

			html_contents = u'<meta charset="%s">\n' % encoding

			# Code Highligght Support
			html_contents += '<link rel="stylesheet" href="http://yandex.st/highlightjs/6.2/styles/default.min.css">\n'
			html_contents += '<script src="http://yandex.st/highlightjs/6.2/highlight.min.js"></script>\n'
			html_contents += "<script>hljs.tabReplace = '  ';hljs.initHighlightingOnLoad();</script>\n"
			
			# LaTeX Support	
			html_contents += "<script type='text/x-mathjax-config'>MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']],processEscapes: true},TeX: { equationNumbers: { autoNumber: 'AMS' } }});</script>\n"
			html_contents += '<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>\n'
			
			# Main Html
			html_contents += markdown_html			


			new_view = self.view.window().new_file()
			new_edit = new_view.begin_edit()
			new_view.insert(new_edit, 0, html_contents)
			new_view.end_edit(new_edit)
