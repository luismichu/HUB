from package import log, icon_stray
import os, sys, imp

# Variables
work_dir = 'C:/MyApps'
expected_class = 'HubRun'

def check_projects(project_names):
	project_class_dict = dict()

	for project in project_names:
		project_dir = work_dir + '/' + project
		files = [file for file in os.listdir(project_dir) if os.path.isfile(project_dir + '/' + file)]

		found_exec = False
		i = 0
		while not found_exec and i < len(files):
			file_name, file_ext = os.path.splitext(files[i])

			if file_ext.lower() == '.py' or file_ext.lower() == '.pyc':
				try:
					imp_project = imp.load_source(file_name, project_dir + '/' + file_name + file_ext)

					if hasattr(imp_project, expected_class):
						project_class_dict.update({project : getattr(imp_project, expected_class)()})

						found_exec = True

					else:
						log.warning('The file', files[i], 'does not have the main class', expected_class)
				
				except ImportError as ie:
					log.warning('Import failed:', ie)

			i += 1

		if not found_exec:
			log.warning('The app', project, 'is in error')

	return project_class_dict

def main():
	try:
		# Initializing logs file
		log.log_name = os.getcwd() + '/Log' + log.get_date() + '.txt'

		log.log('Initializing HUB...')

		log.log('Initializing apps...')
		if os.path.exists(work_dir) and os.path.isdir(work_dir):
			project_names = next(os.walk(work_dir))[1]
		else:
			raise FileNotFoundError

		project_class_dict = check_projects(project_names)
		project_names = list(project_class_dict.keys())

		if len(project_names) <= 0:
			raise IndexError
		elif len(project_names) == 1:
			log.log('Loaded 1 app:', project_names[0])
		else:
			log.log('Loaded', str(len(project_names)), 'apps:')
			[print(project) for project in project_names]

		log.log('Initializing icon stray...')

		menu = tuple()
		for project, project_class in project_class_dict.items():
			menu += (icon_stray.SuperMenuItem(project, (icon_stray.MenuItem('Running', project_class.run, True), 
													icon_stray.MenuItem('Paused', project_class.pause),
													icon_stray.MenuItem('Stopped', project_class.stop))),)
			project_class.run()

		stray = icon_stray.IconStray(menu, 'App Hub')

		log.log('Icon stray running')

		stray.run_no_threaded()



		stray.notify()

	except FileNotFoundError as fnfe:
		log.error('The file or directory does not exist. Exiting...\n{0}'.format(fnfe))

	except IndexError:
		log.error('There are no projects in', work_dir)

	except Exception as e:
		log.error('An exception has ocurred,', e)
		raise e
	

if __name__ == '__main__':
	main()