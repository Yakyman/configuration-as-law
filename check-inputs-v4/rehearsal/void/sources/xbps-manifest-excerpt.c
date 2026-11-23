/* Source: https://raw.githubusercontent.com/void-linux/xbps/master/bin/xbps-create/main.c ; retrieved 2026-11-23 UTC. */
process_xentry(enum entry_type type, const char *mutable_files)
{
	xbps_array_t a;
	xbps_dictionary_t d;
	struct xentry *xe;
	char *p, *saveptr, *args, *tok;
	bool found = false, mutable_found = false;

	a = xbps_array_create();
	if (a == NULL)
		die("xbps_array_create");

	TAILQ_FOREACH_REVERSE(xe, &xentry_list, xentry_head, entries) {
		if (xe->type != type)
			continue;

		found = true;
		d = xbps_dictionary_create();
		if (d == NULL)
			die("xbps_dictionary_create");
		/* sanitize file path */
		p = strchr(xe->file, '.') + 1;
		/*
		 * Find out if this file is mutable.
		 */
		if (mutable_files) {
			if ((strchr(mutable_files, ' ') == NULL) &&
			    (strcmp(mutable_files, p) == 0))
				xbps_dictionary_set_bool(d, "mutable", true);
			else {
				args = strdup(mutable_files);
				if (args == NULL)
					die("strdup");
				for ((tok = strtok_r(args, " ", &saveptr)); tok;
				    (tok = strtok_r(NULL, " ", &saveptr))) {
					if (strcmp(tok, p) == 0) {
						mutable_found = true;
						break;
					}
				}
				free(args);
				if (mutable_found) {
					xbps_dictionary_set_bool(d, "mutable",
					    true);
					mutable_found = false;
				}
			}
		}
		xbps_dictionary_set_cstring(d, "file", p);
		if (xe->target)
			xbps_dictionary_set_cstring(d, "target", xe->target);
		if (*xe->sha256)
			xbps_dictionary_set_cstring(d, "sha256", xe->sha256);
		if (xe->size)
			xbps_dictionary_set_uint64(d, "size", xe->size);

		xbps_array_add(a, d);
		xbps_object_release(d);
	}
	if (found)
		xbps_dictionary_set(pkg_filesd, entry_type_str(type), a);

	xbps_object_release(a);
}

